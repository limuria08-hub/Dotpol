import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = {title:'LiOS.Pol — Research',description:'Local-first political intelligence workspace'};
export default function RootLayout({children}:{children:React.ReactNode}) {
  return <html lang="en"><body>{children}</body></html>;
}
