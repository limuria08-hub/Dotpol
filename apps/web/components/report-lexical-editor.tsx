'use client';

import {useCallback} from 'react';
import {$createParagraphNode,$createTextNode,$getRoot,type EditorState} from 'lexical';
import {LexicalComposer} from '@lexical/react/LexicalComposer';
import {PlainTextPlugin} from '@lexical/react/LexicalPlainTextPlugin';
import {ContentEditable} from '@lexical/react/LexicalContentEditable';
import {HistoryPlugin} from '@lexical/react/LexicalHistoryPlugin';
import {OnChangePlugin} from '@lexical/react/LexicalOnChangePlugin';
import {LexicalErrorBoundary} from '@lexical/react/LexicalErrorBoundary';

type Props={
  artifactId:string;
  initialText:string;
  onChange:(text:string)=>void;
};

/**
 * UI-06: Lexical owns only the ephemeral plain-text editing surface.
 * SQLite Artifacts own canonical answers, evidence, revision numbers and exports.
 * Do not persist Lexical editor JSON or HTML as a second document format.
 */
export function ReportLexicalEditor({artifactId,initialText,onChange}:Props){
  const initialConfig={
    namespace:`dotpol-report-${artifactId}`,
    onError:(error:Error)=>{throw error;},
    editorState:()=>{
      const root=$getRoot();
      root.clear();
      for(const line of initialText.split('\n')){
        const paragraph=$createParagraphNode();
        if(line)paragraph.append($createTextNode(line));
        root.append(paragraph);
      }
    },
  };
  const onEditorChange=useCallback((state:EditorState)=>{
    state.read(()=>onChange($getRoot().getTextContent()));
  },[onChange]);
  return <div className="lexical-report-container">
    <LexicalComposer initialConfig={initialConfig}>
      <PlainTextPlugin
        contentEditable={<ContentEditable className="lexical-report-input"
          aria-label="Edit research artifact"
          aria-multiline="true" aria-placeholder="Edit the plain-text report…"/>}
        placeholder={<div className="lexical-report-placeholder" aria-hidden="true">Edit the plain-text report…</div>}
        ErrorBoundary={LexicalErrorBoundary}
      />
      <HistoryPlugin/>
      <OnChangePlugin onChange={onEditorChange} ignoreSelectionChange/>
    </LexicalComposer>
    <p className="lexical-report-note">Plain-text report · Undo: Ctrl/⌘+Z · Redo: Ctrl/⌘+Shift+Z. Save creates a new canonical revision; citations remain linked but human edits require review.</p>
  </div>;
}
