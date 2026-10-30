import {clsx, type ClassValue} from 'clsx';
import {twMerge} from 'tailwind-merge';

// One utility-class merge owner for shadcn-style Radix components.
export function cn(...values:ClassValue[]) {return twMerge(clsx(values));}
