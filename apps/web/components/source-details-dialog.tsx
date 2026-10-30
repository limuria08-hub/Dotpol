'use client';
import * as React from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import {FileText, X} from 'lucide-react';
import {Button} from './ui/button';

type SourceSummary={id:string;name:string;sha256:string;kind:string;status:string;origin:string};

export function SourceDetailsDialog({source}:{source:SourceSummary}){
 return <Dialog.Root>
  <Dialog.Trigger asChild>
   <Button variant="ghost" size="sm" aria-label={`Inspect source ${source.name}`}>
    <FileText size={15} aria-hidden="true"/> Source details
   </Button>
  </Dialog.Trigger>
  <Dialog.Portal>
   <Dialog.Overlay className="fixed inset-0 z-40 bg-black/70" />
   <Dialog.Content className="fixed left-1/2 top-1/2 z-50 max-h-[min(90vh,650px)] w-[min(calc(100vw-32px),560px)] -translate-x-1/2 -translate-y-1/2 overflow-auto rounded-xl border border-[#40536b] bg-[#121e2d] p-6 text-[#edf2f9] shadow-2xl focus:outline-none"
    aria-describedby={`source-description-${source.id}`}>
    <div className="flex items-start justify-between gap-4">
     <div className="min-w-0">
      <Dialog.Title className="break-words text-lg font-semibold">Source provenance</Dialog.Title>
      <Dialog.Description id={`source-description-${source.id}`} className="mt-1 break-words text-sm text-[#a7bad0]">
       {source.name}
      </Dialog.Description>
     </div>
     <Dialog.Close asChild><Button variant="ghost" size="icon" aria-label="Close source details"><X size={18}/></Button></Dialog.Close>
    </div>
    <dl className="mt-5 grid gap-3 text-sm">
     <div><dt className="text-[#8ea4b9]">Source ID</dt><dd className="mt-1 break-all font-mono">{source.id}</dd></div>
     <div><dt className="text-[#8ea4b9]">Content SHA-256</dt><dd className="mt-1 break-all font-mono">{source.sha256}</dd></div>
     <div><dt className="text-[#8ea4b9]">Type and status</dt><dd className="mt-1">{source.kind.toUpperCase()} · {source.status}</dd></div>
     <div><dt className="text-[#8ea4b9]">Imported from</dt><dd className="mt-1 break-words">{source.origin||'Not recorded'}</dd></div>
    </dl>
    <p className="mt-5 text-xs leading-relaxed text-[#a7bad0]">A hash identifies imported content; it does not prove a document is correct or trustworthy. Review claims against permitted primary sources.</p>
   </Dialog.Content>
  </Dialog.Portal>
 </Dialog.Root>
}
