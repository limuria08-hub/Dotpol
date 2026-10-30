'use client';
import {useCallback, useMemo} from 'react';
import {
 AssistantRuntimeProvider, useExternalStoreRuntime,
 ThreadPrimitive, MessagePrimitive, ComposerPrimitive,
 type AppendMessage, type ThreadMessageLike,
} from '@assistant-ui/react';
import {ArrowUp, PanelRightOpen} from 'lucide-react';

export type ResearchArtifactPreview={
 id:string; question:string; answer:string; created_at:string;
 revision:number; generation_method:string; review_status:string;
 evidence:readonly {source_id:string; source_name:string; line:number; sha256:string; excerpt:string}[];
};

type SavedMessage={id:string;role:'user'|'assistant';text:string;createdAt:Date};
type Props={
 artifacts:readonly ResearchArtifactPreview[];
 onSubmit:(question:string)=>Promise<void>;
 onOpen:(artifactId:string)=>void;
 onDraftChange:()=>void;
 isRunning:boolean;
 isSendDisabled:boolean;
};

/** UI-03: assistant-ui is only a renderer of canonical Dotpol Artifacts.
 * No external history adapter, managed cloud, chat DB, AI SDK transport or
 * direct provider call. The host remains responsible for requests/consent.
 */
export function AssistantResearchThread({artifacts,onSubmit,onOpen,onDraftChange,isRunning,isSendDisabled}:Props){
 const messages=useMemo<SavedMessage[]>(()=>artifacts.slice().reverse().flatMap(a=>[
  {id:`question:${a.id}`,role:'user' as const,text:a.question,createdAt:new Date(a.created_at)},
  {id:`artifact:${a.id}`,role:'assistant' as const,text:a.answer,createdAt:new Date(a.created_at)},
 ]),[artifacts]);

 const convertMessage=useCallback((m:SavedMessage):ThreadMessageLike=>({
  id:m.id,role:m.role,createdAt:m.createdAt,content:[{type:'text',text:m.text}],
 }),[]);

 const onNew=useCallback(async (message:AppendMessage)=>{
  // An external-store action does not imply authorization to send evidence:
  // the host's existing one-request consent check applies to every request.
  const text=message.content.filter((part):part is Extract<typeof part,{type:'text'}>=>part.type==='text')
   .map(part=>part.text).join('\n').trim();
  if(!text)return;
  await onSubmit(text);
 },[onSubmit]);

 const runtime=useExternalStoreRuntime({
  messages,convertMessage,onNew,isRunning,isSendDisabled,
 });
 return <AssistantRuntimeProvider runtime={runtime}>
  <ThreadPrimitive.Root className="assistant-research-thread" aria-label="Assistant research conversation">
   <ThreadPrimitive.Viewport className="assistant-thread-viewport" turnAnchor="bottom">
    {artifacts.length===0?<p className="hint">Import a permitted source and ask a question. Responses will be saved under the project's canonical Artifact IDs.</p>:null}
    <ThreadPrimitive.Messages>
     {({message})=>message.role==='user'?
      <MessagePrimitive.Root className="assistant-message assistant-message-user">
       <div className="assistant-message-content"><MessagePrimitive.Parts/></div>
      </MessagePrimitive.Root>:
      <MessagePrimitive.Root className="assistant-message assistant-message-answer">
       <div className="assistant-message-content"><MessagePrimitive.Parts/></div>
       {message.id.startsWith('artifact:')?(()=>{
        const id=message.id.slice('artifact:'.length);
        const artifact=artifacts.find(a=>a.id===id);
        return artifact?<div className="assistant-artifact-actions">
         <span className="assistant-evidence-label">
          {artifact.generation_method==='ai-synthesis'?'AI synthesis':artifact.generation_method==='no-evidence'?'No evidence':'Evidence only'}
          {' · '}{artifact.evidence.length} source excerpts · rev {artifact.revision}
          {artifact.review_status==='user-edited-unverified'?' · Human-edited; claims unverified':''}
         </span>
         <button type="button" aria-label={`Open artifact ${id} in workbench`}
          onClick={()=>onOpen(id)}><PanelRightOpen size={15} aria-hidden="true"/> Open in workbench</button>
        </div>:null;
       })():null}
      </MessagePrimitive.Root>}
    </ThreadPrimitive.Messages>
   </ThreadPrimitive.Viewport>
   <ComposerPrimitive.Root className="assistant-composer" aria-label="Assistant research composer">
    <ComposerPrimitive.Input aria-label="Assistant research question"
     placeholder="Ask a question about project sources…" onInput={onDraftChange}
     className="assistant-composer-input" rows={2}/>
    <ComposerPrimitive.Send className="assistant-composer-send" aria-label="Send assistant research question" type="submit">
     <ArrowUp size={17} aria-hidden="true"/> Ask AI
    </ComposerPrimitive.Send>
   </ComposerPrimitive.Root>
  </ThreadPrimitive.Root>
 </AssistantRuntimeProvider>;
}
