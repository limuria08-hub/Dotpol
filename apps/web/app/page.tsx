'use client';
import {useEffect, useRef, useState} from 'react';

const API='http://127.0.0.1:8765';
function toBase64(bytes:Uint8Array){let data='';for(let i=0;i<bytes.length;i+=16384)data+=String.fromCharCode(...bytes.subarray(i,i+16384));return btoa(data)}
type Project={id:string,title:string,created_at:string};
type Source={id:string,name:string,sha256:string,kind:string,status:string,origin:string};
type Evidence={source_id:string,source_name:string,sha256:string,line:number,excerpt:string};
type Artifact={id:string,question:string,answer:string,evidence:Evidence[],created_at:string,generation_method:string,model_id:string|null,revision:number,updated_at:string,review_status:string};
type ArtifactRevision={revision:number,answer:string,saved_at:string,origin:'generated'|'user-edited'};
type ModelStatus={status:string,configured:boolean,provider?:string,model?:string|null,message:string};
type OpenClawStatus={component:'openclaw',required_for_release:boolean,ready:boolean,status:string,detail:string};
async function api<T>(path:string,method='GET',body?:unknown):Promise<T> {
 const response=await fetch(API+path,{method,headers:{'Content-Type':'application/json','X-Dotpol-Local':'1'},body:body?JSON.stringify(body):undefined,cache:'no-store'});
 const data=await response.json();
 if(!response.ok)throw new Error(data.detail||'Local API request failed');
 return data as T;
}

export default function Home(){
 const sourceInputRef=useRef<HTMLInputElement>(null);
 const [projects,setProjects]=useState<Project[]>([]);
 const [project,setProject]=useState<Project|null>(null);
 const [sources,setSources]=useState<Source[]>([]);
 const [artifacts,setArtifacts]=useState<Artifact[]>([]);
 const [selected,setSelected]=useState<Artifact|null>(null);
 const [revisions,setRevisions]=useState<ArtifactRevision[]>([]);
 const [editing,setEditing]=useState(false);
 const [draft,setDraft]=useState('');
 const [title,setTitle]=useState('Political research');
 const [question,setQuestion]=useState('');
 const [message,setMessage]=useState('Connect the local API on port 8765 to begin.');
 const [loading,setLoading]=useState(false);
 const [ai,setAi]=useState<ModelStatus|null>(null);
 const [evidenceOnly,setEvidenceOnly]=useState(false);
 const [remoteConsent,setRemoteConsent]=useState(false);
 const [probeStatus,setProbeStatus]=useState('');
 const [openClaw,setOpenClaw]=useState<OpenClawStatus|null>(null);
 const [checkingOpenClaw,setCheckingOpenClaw]=useState(false);
 async function refresh(){try{
  const list=await api<Project[]>('/api/projects');setProjects(list);
  setMessage('Local research engine connected.');
  const state=await api<ModelStatus>('/api/ai/status');setAi(state);
 }catch(e){setMessage((e as Error).message)}}
 async function load(p:Project){setProject(p);setSelected(null);setRevisions([]);setEditing(false);setDraft('');setRemoteConsent(false);
  try {const [s,a]=await Promise.all([api<Source[]>(`/api/projects/${p.id}/sources`),api<Artifact[]>(`/api/projects/${p.id}/artifacts`)]);
   setSources(s);setArtifacts(a);
  }catch(e){setMessage((e as Error).message)}
 }
 useEffect(()=>{void refresh()},[]);
 async function create(){setLoading(true);try{
  const p=await api<Project>('/api/projects','POST',{title});
  setProjects(old=>[p,...old]);await load(p);setMessage('Project created and saved locally.');
 }catch(e){setMessage((e as Error).message)}finally{setLoading(false)}}
 async function importFile(file:File|null){if(!project||!file)return;
  setLoading(true);try{
   const ext=file.name.split('.').pop()?.toLowerCase();if(!['txt','csv','json','pdf','docx'].includes(ext||''))throw new Error('Choose a TXT, CSV, JSON, PDF or DOCX file');
   if(file.size>1024*1024)throw new Error('Source files must be ≤ 1 MiB in this preview');
   if(ext==='pdf'||ext==='docx'){
    const content_base64=toBase64(new Uint8Array(await file.arrayBuffer()));
    await api(`/api/projects/${project.id}/documents`,'POST',{name:file.name,kind:ext,content_base64});
   }else{
    await api(`/api/projects/${project.id}/sources`,'POST',{name:file.name,kind:ext,content:await file.text(),origin:'user-upload'});
   }
   await load(project);setMessage(`Imported ${file.name} with source checksum.`);
  }catch(e){setMessage((e as Error).message)}finally{setLoading(false)}
 }
 async function ask(){if(!project||!question.trim())return;setLoading(true);
  try{const res=await api<{artifact:Artifact,retrieval_mode?:string,retrieval_degraded?:string|null}>(`/api/projects/${project.id}/research`,'POST',{question,mode:evidenceOnly?'extractive':'auto',allow_remote_evidence:remoteConsent && ai?.provider==='openai-compatible'});
   void openArtifact(res.artifact);setArtifacts(old=>[res.artifact,...old]);setQuestion('');setRemoteConsent(false);setMessage(res.artifact.generation_method==='ai-synthesis'?'AI research saved with verified source references.':res.artifact.generation_method==='no-evidence'?'No matching evidence. No political claims were generated.':'Source evidence saved. Configure a model to enable AI synthesis.');
   if(res.retrieval_degraded)setProbeStatus(res.retrieval_degraded);
  }catch(e){setMessage((e as Error).message)}finally{setLoading(false)}
 }
 async function probe(){try{setProbeStatus('Checking local Ollama…');const result=await api<{status:string,detail:string,ready:boolean}>('/api/ai/probe-local','POST',{});setProbeStatus(`${result.status}: ${result.detail}`)}catch(e){setProbeStatus((e as Error).message)}}
 async function checkOpenClaw(){
  if(checkingOpenClaw)return;
  setCheckingOpenClaw(true);
  try{
   const state=await api<OpenClawStatus>('/api/openclaw/status');
   setOpenClaw(state);
  }catch{
   // Do not show raw gateway or HTTP errors in the UI.
   setOpenClaw({component:'openclaw',required_for_release:true,ready:false,status:'unreachable',
    detail:'Could not verify the local OpenClaw gateway.'});
  }finally{setCheckingOpenClaw(false)}
 }
 async function openArtifact(a:Artifact){
  setSelected(a);setDraft(a.answer);setEditing(false);setRevisions([]);
  if(!project)return;
  try{
   setRevisions(await api<ArtifactRevision[]>(`/api/projects/${project.id}/artifacts/${a.id}/revisions`));
  }catch(e){setMessage((e as Error).message)}
 }
 async function saveRevision(){
  if(!project||!selected||!draft.trim()||loading)return;
  setLoading(true);
  try{
   const updated=await api<Artifact>(`/api/projects/${project.id}/artifacts/${selected.id}`,'PATCH',
    {answer:draft,expected_revision:selected.revision});
   setSelected(updated);setArtifacts(old=>old.map(a=>a.id===updated.id?updated:a));
   setEditing(false);setMessage(`Saved artifact revision ${updated.revision}. Human edits are not automatically evidence-verified.`);
   setRevisions(await api<ArtifactRevision[]>(`/api/projects/${project.id}/artifacts/${updated.id}/revisions`));
  }catch(e){setMessage((e as Error).message + ' Your unsaved draft is preserved.');}
  finally{setLoading(false)}
 }
 function exportArtifact(a:Artifact){const blob=new Blob([JSON.stringify(a,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=`dotpol-research-${a.id.slice(0,8)}.json`;
  link.click();URL.revokeObjectURL(url);
 }
 return <div className="shell">
  <aside className="sidebar"><div className="brand">LiOS<span>.Pol</span></div><p className="eyebrow">POLITICAL INTELLIGENCE</p>
   <div className="side-section"><h3>Projects</h3><input aria-label="New project name" value={title} onChange={e=>setTitle(e.target.value)} maxLength={180}/>
    <button disabled={loading} onClick={create}>+ New project</button></div>
   <div className="project-list">{projects.map(p=><button key={p.id} className={project?.id===p.id?'active':''} onClick={()=>load(p)}>{p.title}</button>)}</div>
   <section className="gateway-status" aria-label="Required OpenClaw gateway">
    <div className="gateway-title"><strong>OpenClaw</strong><span>Required</span></div>
    <p role="status" aria-live="polite" className={openClaw?.ready?'gateway-ready':'gateway-detail'}>
     {checkingOpenClaw?'Checking local gateway…':openClaw?.detail||'Local gateway not checked'}
    </p>
    <button type="button" disabled={checkingOpenClaw} onClick={()=>{void checkOpenClaw()}}>
     {checkingOpenClaw?'Checking…':'Check gateway'}
    </button>
   </section>
   <div className="side-footer"><span className="dot"/> Local research preview</div>
  </aside>
  <main className="main"><header><div><p className="eyebrow">WORKSPACE / RESEARCH</p><h1>{project?.title||'Your political research workspace'}</h1></div><span className="label">{ai?.configured?`AI · ${ai.model} (configured)`:'AI · model not configured'}</span></header>
   <p role="status" className="status">{message}</p>
   {!project?<section className="empty"><h2>Create or open a project</h2><p>Import authorized source data and examine verifiable research excerpts. No paid API or cloud account required.</p></section>:
   <div className="columns"><section className="pane"><h2>Sources</h2><p className="hint">TXT, CSV, JSON, PDF or DOCX. PDF/DOCX require optional local Docling.</p>
    <div className="upload-control"><button type="button" className="upload" disabled={loading} onClick={()=>sourceInputRef.current?.click()}>Import source</button><input ref={sourceInputRef} className="file-input-hidden" type="file" tabIndex={-1} accept=".txt,.csv,.json,.pdf,.docx" disabled={loading} onChange={e=>{void importFile(e.target.files?.[0]||null);e.target.value=''}} /></div>
    <ul className="source-list">{sources.map(s=><li key={s.id}><strong>{s.name}</strong><small>{s.kind.toUpperCase()} · {s.status}<br/>SHA-256: {s.sha256.slice(0,16)}…</small></li>)}</ul>
    <h2>Saved research</h2><div className="artifact-list">{artifacts.map(a=><button key={a.id} onClick={()=>{void openArtifact(a)}}>{a.question}<small>{new Date(a.updated_at||a.created_at).toLocaleString()} · rev {a.revision}</small></button>)}</div>
   </section><section className="workspace"><h2>Ask LiOS.Pol AI</h2><p className="hint">AI uses retrieved project sources and verifiable citations. If no model is configured, evidence-only research remains available.</p><div className="ai-control"><label><input type="checkbox" checked={evidenceOnly} onChange={e=>setEvidenceOnly(e.target.checked)}/> Evidence only (skip AI)</label><span>{ai?.configured?`Provider: ${ai.provider}`:'Connect local Ollama to enable AI synthesis'}</span></div>
    {ai?.provider==='ollama'&&ai.configured?<div className="ai-control"><button type="button" disabled={loading} onClick={()=>{void probe()}}>Check local model</button><span role="status">{probeStatus}</span></div>:null}
    {ai?.provider==='openai-compatible' && ai.configured && !evidenceOnly?<label className="ai-control remote-consent"><input type="checkbox" checked={remoteConsent} onChange={e=>setRemoteConsent(e.target.checked)}/> Approve sending the retrieved source excerpts and question to my configured external model for this one request.</label>:null}
    <div className="ask"><input aria-label="Research question" placeholder="Search local political datasets and documents" value={question} onChange={e=>setQuestion(e.target.value)} onKeyDown={e=>{if(e.key==='Enter')void ask()}} /><button disabled={loading||!question.trim()||(ai?.configured===true&&ai.provider==='openai-compatible'&&!evidenceOnly&&!remoteConsent)} onClick={ask}>{loading?'Working…':'Ask AI'}</button></div>
    {selected?<article className="result"><div className="result-head"><span>{selected.generation_method==='ai-synthesis'?`AI synthesis · ${selected.model_id||'model unspecified'}`:selected.generation_method==='no-evidence'?'Evidence unavailable':'Evidence-only research'}</span><button onClick={()=>exportArtifact(selected)}>Export JSON</button></div><h3>{selected.question}</h3><div className="artifact-edit-bar"><span>Revision {selected.revision} · {selected.review_status==='user-edited-unverified'?'Edited — citations need review': 'Source-linked original — claims not fact-checked'}</span>
     {!editing?<button type="button" onClick={()=>setEditing(true)}>Edit in workbench</button>:<><button type="button" disabled={loading||!draft.trim()} onClick={()=>{void saveRevision()}}>Save revision</button><button type="button" disabled={loading} onClick={()=>{setEditing(false);setDraft(selected.answer)}}>Cancel</button></>}
    </div>
    {editing?<textarea aria-label="Edit research artifact" className="artifact-editor" value={draft} onChange={e=>setDraft(e.target.value)} maxLength={100000} />:<pre>{selected.answer}</pre>}
    <h4>Source evidence and provenance</h4>
     {selected.evidence.length?selected.evidence.map((e,i)=><details key={`${e.source_id}-${e.line}-${i}`}><summary>[{i+1}] {e.source_name} · line {e.line}</summary><blockquote>{e.excerpt}</blockquote><small>Source ID: {e.source_id} · SHA-256: {e.sha256}</small></details>):<p className="hint">No matching evidence. The system did not invent an answer.</p>}
     <details><summary>Revision history ({revisions.length})</summary>{revisions.map(rev=><div className="revision-entry" key={rev.revision}><strong>Revision {rev.revision} · {rev.origin}</strong><small>{new Date(rev.saved_at).toLocaleString()}</small><pre>{rev.answer}</pre></div>)}</details>
    </article>:<div className="empty"><h3>Start with a source</h3><p>Upload a text or table file, ask a question, and open a saved evidence-linked artifact here.</p></div>}
   </section></div>}
   <footer>Phase 1 · AI-native research foundation · Local-first · Evidence verification required</footer>
  </main>
 </div>
}
