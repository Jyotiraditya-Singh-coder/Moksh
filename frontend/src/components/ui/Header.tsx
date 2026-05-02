'use client';

import { useEffect } from 'react';
import { useAuth, UserButton } from '@clerk/nextjs';
import Link from 'next/link';
import { useLanguage } from '@/app/contexts/LanguageContext';

export default function Header() {
  const { t } = useLanguage();
  const { isSignedIn } = useAuth();
  useEffect(() => {
    import('bootstrap/dist/js/bootstrap.bundle.min.js' as string);
  }, []);
  return (
    <header className="site-header">
      <nav className="navbar navbar-expand-lg container">
        <Link className="navbar-brand" href="/">EduNex AI</Link>

        {/* Auth buttons - always visible, pinned top-right */}
        <div className="d-flex gap-2 order-lg-last ms-auto me-2 me-lg-0 align-items-center">
          {isSignedIn ? (
            <UserButton afterSignOutUrl="/" />
          ) : (
            <>
              <Link href="/login" className="btn btn-nav-login">{t('navLog')}</Link>
              <Link href="/signup" className="btn btn-nav-signup">{t('navSign')}</Link>
            </>
          )}
        </div>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navMain"
          aria-controls="navMain"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navMain">
          <ul className="navbar-nav ms-auto me-lg-3 gap-1">
            <li className="nav-item"><a className="nav-link active" href="#">{t('navHome')}</a></li>
            <li className="nav-item"><a className="nav-link" href="#features">{t('navFeatures')}</a></li>
            <li className="nav-item"><a className="nav-link" href="#tech">{t('navTech')}</a></li>
            <li className="nav-item"><a className="nav-link" href="#team">{t('navTeam')}</a></li>
            <li className="nav-item"><a className="nav-link" href="#cta">{t('navContact')}</a></li>
          </ul>
        </div>
      </nav>
    </header>
  );
}
