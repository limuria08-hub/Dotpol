'use client';
import {useEffect, useState, type ReactNode} from 'react';
import {Panel, PanelGroup, PanelResizeHandle} from 'react-resizable-panels';
import {GripVertical} from 'lucide-react';

type Props = {
  showWorkbench:boolean;
  conversation:ReactNode;
  workbench:ReactNode;
};

/** P1.08 UI-04 — one view over the existing Project/Artifact records.
 * The panel library owns resizing, not content or backend persistence.
 * Narrow screens stack the SAME React content, without duplicate editors.
 */
export function ResearchSplit({showWorkbench,conversation,workbench}:Props) {
  const [compact,setCompact]=useState(false);
  useEffect(()=>{
    const media=window.matchMedia('(max-width: 1050px)');
    const update=()=>setCompact(media.matches);
    update();
    media.addEventListener('change',update);
    return ()=>media.removeEventListener('change',update);
  },[]);

  if(!showWorkbench) {
    return <div className="research-single">{conversation}</div>;
  }

  if(compact) {
    return <div className="research-stacked">
      {conversation}
      {workbench}
    </div>;
  }

  return <PanelGroup direction="horizontal" autoSaveId="dotpol-p1-chat-workbench"
    className="research-split" aria-label="Research and artifact workbench">
    <Panel id="conversation" order={1} defaultSize={44} minSize={28} className="research-panel">
      {conversation}
    </Panel>
    <PanelResizeHandle className="research-resize-handle"
      aria-label="Resize conversation and artifact workbench" tabIndex={0}>
      <GripVertical size={16} aria-hidden="true"/>
    </PanelResizeHandle>
    <Panel id="workbench" order={2} defaultSize={56} minSize={30} className="research-panel">
      {workbench}
    </Panel>
  </PanelGroup>;
}
