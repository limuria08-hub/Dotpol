'use client';
import {useEffect, useState} from 'react';

const API='http://127.0.0.1:8765';
type Project={id:string,title:string,created_at:string};
type Source={id:string,name:string,sha256:string,kind:string,status:string,origin:string};
type Evidence={source_id:string,source_name:string,sha256:string,line:number,excerpt:string};
type Artifact={id:string,question:string,answer:string,evidence:Evidence[],created_at:string,generation_method:string,model_id:string|null};
type ModelStatus={status:string,configured:boolean,provider?:string,model?:string|null,message:string};
async function api<T>(path:string,method='GET',body?:unknown):Promise<T> {
 const response=await fetch(API+path,{method,headers:{'Content-Type':'application/json','X-Dotpol-Local':'1'},body:body?JSON.stringify(body):undefined,cache:'no-store'});
 const data=await response.json();
 if(!response.ok)throw new Error(data.detail||'Local API request failed');
 return data as T;
}

export default function Home(){
 const [projects,setProjects]=useState<Project[]>([]);
 const [project,setProject]=useState<Project|null>(null);
 const [sources,setSources]=useState<Source[]>([]);
 const [artifacts,setArtifacts]=useState<Artifact[]>([]);
 const [selected,setSelected]=useState<Artifact|null>(null);
 const [title,setTitle]=useState('Political research');
 const [question,setQuestion]=useState('');
 const [message,setMessage]=useState('Connect the local API on port 8765 to begin.');
 const [loading,setLoading]=useState(false);
 const [ai,setAi]=useState<ModelStatus|null>(null);
 const [evidenceOnly,setEvidenceOnly]=useState(false);
 const [remoteConsent,setRemoteConsent]=useState(false);
 const [probeStatus,setProbeStatus]=useState('');
 async function refresh(){try{
  const list=await api<Project[]>('/api/projects');setProjects(list);
  setMessage('Local research engine connected.');
  const state=await api<ModelStatus>('/api/ai/status');setAi(state);
 }catch(e){setMessage((e as Error).message)}}
 async function load(p:Project){setProject(p);setSelected(null);setRemoteConsent(false);
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
   const ext=file.name.split('.').pop()?.toLowerCase();if(!['txt','csv','json'].includes(ext||''))throw new Error('Choose a TXT, CSV or JSON file');
   if(file.size>1024*1024)throw new Error('Source files must be ≤ 1 MiB in this preview');
   await api(`/api/projects/${project.id}/sources`,'POST',{name:file.name,kind:ext,content:await file.text(),origin:'user-upload'});
   await load(project);setMessage(`Imported ${file.name} with source checksum.`);
  }catch(e){setMessage((e as Error).message)}finally{setLoading(false)}
 }
 async function ask(){if(!project||!question.trim())return;setLoading(true);
  try{const res=await api<{artifact:Artifact}>(`/api/projects/${project.id}/research`,'POST',{question,mode:evidenceOnly?'extractive':'auto',allow_remote_evidence:remoteConsent && ai?.provider==='openai-compatible'});
   setSelected(res.artifact);setArtifacts(old=>[res.artifact,...old]);setQuestion('');setRemoteConsent(false);setMessage(res.artifact.generation_method==='ai-synthesis'?'AI research saved with verified source references.':res.artifact.generation_method==='no-evidence'?'No matching evidence. No political claims were generated.':'Source evidence saved. Configure a model to enable AI synthesis.');
  }catch(e){setMessage((e as Error).message)}finally{setLoading(false)}
 }
 async function probe(){try{setProbeStatus('Checking local Ollama…');const result=await api<{status:string,detail:string,ready:boolean}>('/api/ai/probe-local','POST',{});setProbeStatus(`${result.status}: ${result.detail}`)}catch(e){setProbeStatus((e as Error).message)}}
 function exportArtifact(a:Artifact){const blob=new Blob([JSON.stringify(a,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=`dotpol-research-${a.id.slice(0,8)}.json`;
  link.click();URL.revokeObjectURL(url);
 }
 return <div className="shell">
  <aside className="sidebar"><div className="brand">LiOS<span>.Pol</span></div><p className="eyebrow">POLITICAL INTELLIGENCE</p>
   <div className="side-section"><h3>Projects</h3><input aria-label="New project name" value={title} onChange={e=>setTitle(e.target.value)} maxLength={180}/>
    <button disabled={loading} onClick={create}>+ New project</button></div>
   <div className="project-list">{projects.map(p=><button key={p.id} className={project?.id===p.id?'active':''} onClick={()=>load(p)}>{p.title}</button>)}</div>
   <div className="side-footer"><span className="dot"/> Local-only research preview</div>
  </aside>
  <main className="main"><header><div><p className="eyebrow">WORKSPACE / RESEARCH</p><h1>{project?.title||'Your political research workspace'}</h1></div><span className="label">{ai?.configured?`AI · ${ai.model} (configured)`:'AI · model not configured'}</span></header>
   <p role="status" className="status">{message}</p>
   {!project?<section className="empty"><h2>Create or open a project</h2><p>Import authorized source data and examine verifiable research excerpts. No paid API or cloud account required.</p></section>:
   <div className="columns"><section className="pane"><h2>Sources</h2><p className="hint">TXT, CSV or JSON. Files stay in your local SQLite database.</p>
    <label className="upload">Import source<input type="file" accept=".txt,.csv,.json" disabled={loading} onChange={e=>{void importFile(e.target.files?.[0]||null);e.target.value=''}} /></label>
    <ul className="source-list">{sources.map(s=><li key={s.id}><strong>{s.name}</strong><small>{s.kind.toUpperCase()} · {s.status}<br/>SHA-256: {s.sha256.slice(0,16)}…</small></li>)}</ul>
    <h2>Saved research</h2><div className="artifact-list">{artifacts.map(a=><button key={a.id} onClick={()=>setSelected(a)}>{a.question}<small>{new Date(a.created_at).toLocaleString()}</small></button>)}</div>
   </section><section className="workspace"><h2>Ask LiOS.Pol AI</h2><p className="hint">AI uses retrieved project sources and verifiable citations. If no model is configured, evidence-only research remains available.</p><div className="ai-control"><label><input type="checkbox" checked={evidenceOnly} onChange={e=>setEvidenceOnly(e.target.checked)}/> Evidence only (skip AI)</label><span>{ai?.configured?`Provider: ${ai.provider}`:'Connect local Ollama to enable AI synthesis'}</span></div>
    {ai?.provider==='ollama'&&ai.configured?<div className="ai-control"><button type="button" disabled={loading} onClick={()=>{void probe()}}>Check local model</button><span role="status">{probeStatus}</span></div>:null}
    {ai?.provider==='openai-compatible' && ai.configured && !evidenceOnly?<label className="ai-control remote-consent"><input type="checkbox" checked={remoteConsent} onChange={e=>setRemoteConsent(e.target.checked)}/> Approve sending the retrieved source excerpts and question to my configured external model for this one request.</label>:null}
    <div className="ask"><input aria-label="Research question" placeholder="Search local political datasets and documents" value={question} onChange={e=>setQuestion(e.target.value)} onKeyDown={e=>{if(e.key==='Enter')void ask()}} /><button disabled={loading||!question.trim()||(ai?.configured===true&&ai.provider==='openai-compatible'&&!evidenceOnly&&!remoteConsent)} onClick={ask}>{loading?'Working…':'Ask AI'}</button></div>
    {selected?<article className="result"><div className="result-head"><span>{selected.generation_method==='ai-synthesis'?`AI synthesis · ${selected.model_id||'model unspecified'}`:selected.generation_method==='no-evidence'?'Evidence unavailable':'Evidence-only research'}</span><button onClick={()=>exportArtifact(selected)}>Export JSON</button></div><h3>{selected.question}</h3><pre>{selected.answer}</pre><h4>Source evidence and provenance</h4>
     {selected.evidence.length?selected.evidence.map((e,i)=><details key={`${e.source_id}-${e.line}-${i}`}><summary>[{i+1}] {e.source_name} · line {e.line}</summary><blockquote>{e.excerpt}</blockquote><small>Source ID: {e.source_id} · SHA-256: {e.sha256}</small></details>):<p className="hint">No matching evidence. The system did not invent an answer.</p>}
    </article>:<div className="empty"><h3>Start with a source</h3><p>Upload a text or table file, ask a question, and open a saved evidence-linked artifact here.</p></div>}
   </section></div>}
   <footer>Phase 1 · AI-native research foundation · Local-first · Evidence verification required</footer>
  </main>
 </div>
}
