'use client';

import Link from 'next/link';
import { useAuth } from '@clerk/nextjs';
import { useLanguage } from '@/app/contexts/LanguageContext';

export default function HeroSection() {
  const { t } = useLanguage();
  const { isSignedIn } = useAuth();
  // The handleGetStarted function is no longer used with the new JSX structure
  // that uses a Link for "Get Started" and a separate button for "Demo".
  // Therefore, it can be removed.
  // const handleGetStarted = () => {
  //   const scrollTarget = document.querySelector('.scroll-experience');
  //   if (scrollTarget) {
  //     const totalHeight = scrollTarget.scrollHeight;
  //     window.scrollTo({ top: totalHeight, behavior: 'smooth' });
  //   }
  // };

  return (
    <>
      <h1 className="hero-title">{t('heroTitle')}</h1>
      
      <div className="hero-extras">
        <p className="hero-desc">
          {t('heroDesc')}
        </p>
        <div className="hero-actions">
          <Link href={isSignedIn ? '/dashboard' : '/signup'} className="hero-cta">{t('heroStarted')}</Link>
        </div>
      </div>
    </>
  );
}
