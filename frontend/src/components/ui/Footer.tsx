'use client';

import { useLanguage } from '@/app/contexts/LanguageContext';

export default function Footer() {
  const { t } = useLanguage();
  const year = new Date().getFullYear();
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="row g-4">
          <div className="col-lg-4">
            <span className="footer-brand">EduNex AI</span>
            <p className="mt-2">{t('footerDesc')}</p>
          </div>
          <div className="col-6 col-lg-2">
            <h6 className="mb-3" style={{ color: 'var(--text-primary)' }}>{t('footerProduct')}</h6>
            <ul className="list-unstyled d-flex flex-column gap-2">
              <li><a href="#">{t('navFeatures')}</a></li>
              <li><a href="#">{t('footerPricing')}</a></li>
              <li><a href="#">{t('footerIntegrations')}</a></li>
            </ul>
          </div>
          <div className="col-6 col-lg-2">
            <h6 className="mb-3" style={{ color: 'var(--text-primary)' }}>{t('footerCompany')}</h6>
            <ul className="list-unstyled d-flex flex-column gap-2">
              <li><a href="#">{t('footerAbout')}</a></li>
              <li><a href="#">{t('footerBlog')}</a></li>
              <li><a href="#">{t('footerCareers')}</a></li>
            </ul>
          </div>
          <div className="col-lg-4">
            <h6 className="mb-3" style={{ color: 'var(--text-primary)' }}>{t('footerStayUpdated')}</h6>
            <p>{t('footerSubscribe')}</p>
            <div className="d-flex gap-2 mt-2">
              <input
                type="email"
                className="form-control"
                placeholder={t('footerEmailPlaceholder')}
                style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', color: 'var(--text-primary)' }}
              />
              <button className="btn btn-primary">{t('footerJoin')}</button>
            </div>
          </div>
        </div>
        <hr style={{ borderColor: 'var(--glass-border)', margin: '2.5rem 0 1rem' }} />
        <p className="text-center mb-0">{t('footerRights')}</p>
      </div>
    </footer>
  );
}
