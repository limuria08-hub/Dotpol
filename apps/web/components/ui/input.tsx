import * as React from 'react';
import {cn} from '../../lib/utils';

export const Input=React.forwardRef<HTMLInputElement,React.ComponentProps<'input'>>(
 ({className,type,...props},ref)=><input ref={ref} type={type}
  className={cn('flex min-h-10 w-full rounded-lg border border-[#40536b] bg-[#152130] px-3 py-2 text-sm text-white placeholder:text-[#9db0c5] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-300 disabled:opacity-50',className)} {...props}/>
);
Input.displayName='Input';
