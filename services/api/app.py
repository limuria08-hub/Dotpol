"""Single localhost FastAPI API. Browser calls cannot bypass origin checks."""
from __future__ import annotations

import os
from pathlib import Path
from starlette.concurrency import run_in_threadpool
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, StrictInt
from fastapi.responses import JSONResponse
from dotpol_platform.store import Store, InvalidInput, NotFound, RevisionConflict
from dotpol_platform.political_identity import initialize as init_entities, register as register_entity, list_entities, get_entity
from dotpol_platform.documents import extract_document, DocumentEngineUnavailable
from dotpol_platform.openclaw_gateway import probe_openclaw, audit_openclaw_security, verify_openclaw_rpc
from dotpol_platform.research import search, ai_research
from dotpol_platform.cross_source import compare_sources
from dotpol_platform.election_results import initialize as init_election_results, import_results, list_imports, get_import
from dotpol_platform.ai import (status as model_status, probe_local_model, AIUnavailable, UngroundedAnswer, RemoteEvidenceConsentRequired)

DB_PATH = Path(os.getenv('DOTPOL_DATA_DIR', str(Path.home()/'.dotpol')))/'dotpol.sqlite3'
ALLOWED_ORIGINS = {'http://localhost:3000','http://127.0.0.1:3000'}


class PoliticalEntityIn(BaseModel):
    kind: Literal['jurisdiction','administrative-area','electoral-area','constituency','boundary-version','polling-station','person','party','alliance','organisation','office','election','contest']
    name: str = Field(min_length=1,max_length=180)
    source_id: str | None = None


class ElectionResultImportIn(BaseModel):
    source_id: str = Field(pattern=r'^[a-f0-9]{32}$')


class ProjectIn(BaseModel):
    title: str = Field(min_length=1,max_length=180)


class SourceIn(BaseModel):
    name: str = Field(min_length=1,max_length=180)
    kind: Literal['txt','csv','json']
    content: str = Field(min_length=1,max_length=1024*1024)
    origin: Literal['user-upload','synthetic-demo']='user-upload'


class DocumentIn(BaseModel):
    name: str = Field(min_length=1, max_length=180)
    kind: Literal['pdf', 'docx']
    content_base64: str = Field(min_length=1, max_length=1398110)


class ArtifactRevisionIn(BaseModel):
    answer: str = Field(min_length=1, max_length=100000)
    expected_revision: StrictInt = Field(ge=1)


class QuestionIn(BaseModel):
    question: str = Field(min_length=1,max_length=2000)
    mode: Literal['auto','ai','extractive'] = 'auto'
    allow_remote_evidence: bool = False


def create_app(db_path: str | Path | None = None) -> FastAPI:
    store=Store(db_path or DB_PATH)
    init_entities(store)
    init_election_results(store)
    app=FastAPI(title='Dotpol Local Gateway',version='0.1.0')
    app.add_middleware(CORSMiddleware,allow_origins=sorted(ALLOWED_ORIGINS),allow_credentials=False,
                       allow_methods=['GET','POST','PATCH'],allow_headers=['X-Dotpol-Local','Content-Type'])

    @app.middleware('http')
    async def localhost_only(request:Request,call_next):
        host=request.headers.get('host','').split(':')[0].lower()
        if host not in {'localhost','127.0.0.1','[::1]','testserver'}:
            return JSONResponse(
                {'detail':'Local host required'},status_code=403)
        origin=request.headers.get('origin')
        if origin and origin not in ALLOWED_ORIGINS:
            return JSONResponse(
                {'detail':'Origin not allowed'},status_code=403)
        if request.method in {'POST','PUT','PATCH','DELETE'} and request.headers.get('x-dotpol-local')!='1':
            return JSONResponse(
                {'detail':'Missing local request header'},status_code=403)
        return await call_next(request)

    @app.exception_handler(InvalidInput)
    async def invalid(request,exc):
        from fastapi.responses import JSONResponse
        return JSONResponse({'detail':str(exc)},status_code=422)

    @app.exception_handler(NotFound)
    async def missing(request,exc):
        from fastapi.responses import JSONResponse
        return JSONResponse({'detail':str(exc)},status_code=404)

    @app.exception_handler(RevisionConflict)
    async def edit_conflict(request,exc):
        return JSONResponse({'detail':str(exc),'status':'revision-conflict'},status_code=409)

    @app.exception_handler(DocumentEngineUnavailable)
    async def docling_missing(request, exc):
        return JSONResponse({'detail':str(exc),'status':'document-engine-unavailable'},status_code=503)

    @app.exception_handler(AIUnavailable)
    async def provider_unavailable(request, exc):
        return JSONResponse({'detail':str(exc),'status':'ai-unavailable'},status_code=503)

    @app.exception_handler(RemoteEvidenceConsentRequired)
    async def remote_consent_required(request, exc):
        return JSONResponse({'detail':str(exc),'status':'remote-consent-required'},status_code=403)

    @app.exception_handler(UngroundedAnswer)
    async def invalid_synthesis(request, exc):
        return JSONResponse({'detail':str(exc),'status':'ungrounded-ai-response'},status_code=422)

    @app.get('/health')
    def health():
        return {'status':'ok','local':True,'version':'0.1.0'}

    @app.get('/api/openclaw/status')
    async def openclaw_status():
        # OpenClaw is required for release. A read-only probe must never
        # install/start the gateway or reveal channel credentials.
        return await run_in_threadpool(probe_openclaw)

    @app.post('/api/openclaw/rpc-check')
    async def openclaw_rpc_check():
        # Uses the installed OpenClaw CLI for its native WS handshake.
        # Only fixed read-only 'status' is called; no gateway credentials
        # or operator session metadata are returned to the browser.
        return await run_in_threadpool(verify_openclaw_rpc)

    @app.post('/api/openclaw/audit')
    async def openclaw_security_audit():
        # Explicit user action only; no --fix, --deep or browser secrets.
        return await run_in_threadpool(audit_openclaw_security)

    @app.get('/api/ai/status')
    def ai_status():
        return model_status()

    @app.post('/api/ai/probe-local')
    async def ai_probe_local():
        return await probe_local_model()

    @app.get('/api/projects')
    def list_projects():
        return store.projects()

    @app.post('/api/projects',status_code=201)
    def create_project(body:ProjectIn):
        return store.create_project(body.title)

    @app.get('/api/projects/{project_id}')
    def get_project(project_id:str):
        return store.project(project_id)

    @app.post('/api/projects/{project_id}/entities',status_code=201)
    def create_entity(project_id:str,body:PoliticalEntityIn):
        return register_entity(store,project_id,body.kind,body.name,body.source_id)

    @app.get('/api/projects/{project_id}/entities')
    def entities(project_id:str,kind:str|None=None):
        return list_entities(store,project_id,kind)

    @app.get('/api/projects/{project_id}/entities/{entity_id}')
    def entity(project_id:str,entity_id:str):
        return get_entity(store,project_id,entity_id)

    @app.post('/api/projects/{project_id}/election-results/import',status_code=201)
    def import_election_results(project_id:str,body:ElectionResultImportIn):
        return import_results(store,project_id,body.source_id)

    @app.get('/api/projects/{project_id}/election-results/imports')
    def election_imports(project_id:str):
        return list_imports(store,project_id)

    @app.get('/api/projects/{project_id}/election-results/imports/{import_id}')
    def election_import(project_id:str,import_id:str):
        return get_import(store,project_id,import_id)

    @app.get('/api/projects/{project_id}/sources')
    def list_sources(project_id:str):
        return store.sources(project_id)

    @app.post('/api/projects/{project_id}/sources',status_code=201)
    def add_source(project_id:str,body:SourceIn):
        return store.import_source(project_id,body.name,body.kind,body.content,body.origin)

    @app.post('/api/projects/{project_id}/documents', status_code=201)
    async def add_document(project_id: str, body: DocumentIn):
        store.project(project_id)
        content, file_hash, engine = await run_in_threadpool(
            extract_document, body.name, body.kind, body.content_base64)
        return store.import_source(project_id, body.name, body.kind, content,
                                   file_sha256=file_hash, extraction_method=engine)

    @app.get('/api/projects/{project_id}/sources/{source_id}')
    def source(project_id:str,source_id:str):
        return store.source(project_id,source_id)

    @app.post('/api/projects/{project_id}/sources/{source_id}/withdraw')
    def withdraw(project_id:str,source_id:str):
        row=store.withdraw(project_id,source_id)
        return {k:v for k,v in row.items() if k!='content'}

    @app.get('/api/projects/{project_id}/search')
    def find(project_id:str,q:str,limit:int=8):
        return search(store,project_id,q,limit)

    @app.post('/api/projects/{project_id}/research')
    async def ask(project_id:str,body:QuestionIn):
        return await ai_research(store,project_id,body.question,body.mode, allow_remote_evidence=body.allow_remote_evidence)

    @app.post('/api/projects/{project_id}/compare')
    def compare(project_id:str,body:QuestionIn):
        return compare_sources(store,project_id,body.question)

    @app.get('/api/projects/{project_id}/artifacts')
    def artifacts(project_id:str):
        return store.artifacts(project_id)

    @app.get('/api/projects/{project_id}/artifacts/{artifact_id}')
    def artifact(project_id:str,artifact_id:str):
        return store.artifact(project_id,artifact_id)

    @app.patch('/api/projects/{project_id}/artifacts/{artifact_id}')
    def revise_artifact(project_id:str,artifact_id:str,body:ArtifactRevisionIn):
        return store.revise_artifact(project_id,artifact_id,body.answer,body.expected_revision)

    @app.get('/api/projects/{project_id}/artifacts/{artifact_id}/revisions')
    def artifact_revisions(project_id:str,artifact_id:str):
        return store.artifact_history(project_id,artifact_id)

    return app

app=create_app()
