import * as React from 'react';
import {Slot} from '@radix-ui/react-slot';
import {cn} from '../../lib/utils';

type Variant='primary'|'secondary'|'outline'|'ghost';
type Size='default'|'sm'|'icon';
type Props=React.ComponentProps<'button'> & {variant?:Variant;size?:Size;asChild?:boolean};

const base='inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-300 disabled:pointer-events-none disabled:opacity-50';
const variants:Record<Variant,string>={
 primary:'bg-[#f3cc6b] text-[#171a21] hover:bg-[#ffe2a1]',
 secondary:'bg-[#27384c] text-[#e8edf4] hover:bg-[#33485f]',
 outline:'border border-[#465b75] bg-transparent text-[#e8edf4] hover:bg-[#25364b]',
 ghost:'bg-transparent text-[#f3cc6b] hover:bg-[#27384c]',
};
const sizes:Record<Size,string>={
 default:'min-h-10 px-4 py-2',
 sm:'min-h-8 px-3 py-1.5 text-xs',
 icon:'size-9 p-2',
};
export const Button=React.forwardRef<HTMLButtonElement,Props>(
 ({variant='secondary',size='default',asChild=false,className,type,...props},ref)=>{
  const Component=asChild?Slot:'button';
  return <Component ref={ref} type={asChild?undefined:(type||'button')}
   className={cn(base,variants[variant],sizes[size],className)} {...props}/>;
 }
);
Button.displayName='Button';
