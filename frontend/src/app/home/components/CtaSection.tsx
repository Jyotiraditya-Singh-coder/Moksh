'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@clerk/nextjs';
import { useLanguage } from '@/app/contexts/LanguageContext';

export default function CtaSection() {
  const { t } = useLanguage();
  const { isSignedIn } = useAuth();
  return (
    <section className="section-normal cta-section">
      <div className="container">
        <h2 className="section-title text-white">{t('ctaTitle')}</h2>
        <p className="section-subtitle text-white/80 mx-auto" style={{ maxWidth: '600px' }}>
          {t('ctaSub')}
        </p>
        <div className="d-flex justify-content-center gap-3 flex-wrap">
          <Link href={isSignedIn ? '/dashboard' : '/signup'} className="btn btn-primary btn-lg px-5">
            Get Started
          </Link>
        </div>
      </div>
    </section>
  );
}
