"""Single localhost FastAPI API. Browser calls cannot bypass origin checks."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from dotpol_platform.store import Store, InvalidInput, NotFound
from dotpol_platform.research import search, research
from dotpol_platform.ai import status as model_status

DB_PATH = Path(os.getenv('DOTPOL_DATA_DIR', str(Path.home()/'.dotpol')))/'dotpol.sqlite3'
ALLOWED_ORIGINS = {'http://localhost:3000','http://127.0.0.1:3000'}


class ProjectIn(BaseModel):
    title: str = Field(min_length=1,max_length=180)


class SourceIn(BaseModel):
    name: str = Field(min_length=1,max_length=180)
    kind: Literal['txt','csv','json']
    content: str = Field(min_length=1,max_length=1024*1024)
    origin: Literal['user-upload','synthetic-demo']='user-upload'


class QuestionIn(BaseModel):
    question: str = Field(min_length=1,max_length=2000)


def create_app(db_path: str | Path | None = None) -> FastAPI:
    store=Store(db_path or DB_PATH)
    app=FastAPI(title='Dotpol Local Gateway',version='0.1.0')
    app.add_middleware(CORSMiddleware,allow_origins=sorted(ALLOWED_ORIGINS),allow_credentials=False,
                       allow_methods=['GET','POST'],allow_headers=['X-Dotpol-Local','Content-Type'])

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

    @app.get('/health')
    def health():
        return {'status':'ok','local':True,'version':'0.1.0'}

    @app.get('/api/ai/status')
    def ai_status():
        return model_status()

    @app.get('/api/projects')
    def list_projects():
        return store.projects()

    @app.post('/api/projects',status_code=201)
    def create_project(body:ProjectIn):
        return store.create_project(body.title)

    @app.get('/api/projects/{project_id}')
    def get_project(project_id:str):
        return store.project(project_id)

    @app.get('/api/projects/{project_id}/sources')
    def list_sources(project_id:str):
        return store.sources(project_id)

    @app.post('/api/projects/{project_id}/sources',status_code=201)
    def add_source(project_id:str,body:SourceIn):
        return store.import_source(project_id,body.name,body.kind,body.content,body.origin)

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
    def ask(project_id:str,body:QuestionIn):
        return research(store,project_id,body.question)

    @app.get('/api/projects/{project_id}/artifacts')
    def artifacts(project_id:str):
        return store.artifacts(project_id)

    @app.get('/api/projects/{project_id}/artifacts/{artifact_id}')
    def artifact(project_id:str,artifact_id:str):
        return store.artifact(project_id,artifact_id)

    return app

app=create_app()
