'use client';
import { LanguageProvider } from '@/app/contexts/LanguageContext';

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <LanguageProvider>
      {children}
    </LanguageProvider>
  );
}
