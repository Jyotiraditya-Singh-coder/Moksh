'use client';

import React from 'react';
import { useLanguage } from '@/app/contexts/LanguageContext';

const ABOUT_TEXT =
  'EduNex AI is a next-generation education platform that harnesses artificial intelligence to deliver deeply personalized learning experiences. From adaptive challenges to predictive analytics, we empower institutions and learners alike.';

const FEATURES = [
  { icon: '\uD83E\uDDE0', title: 'AI-Powered Curriculum', desc: 'Dynamically generated learning paths tailored to individual student profiles and goals.' },
  { icon: '\uD83D\uDCCA', title: 'Real-Time Analytics', desc: 'Comprehensive dashboards for educators to monitor progress and intervene early.' },
  { icon: '\uD83C\uDF10', title: 'Multilingual Support', desc: 'Content and voice tutoring available in 50+ languages for global accessibility.' },
  { icon: '\uD83D\uDD12', title: 'Secure & Private', desc: 'Enterprise-grade security ensuring student data remains protected at all times.' },
  { icon: '\u26A1', title: 'Instant Feedback', desc: 'AI-driven evaluation providing immediate, actionable feedback on assignments.' },
  { icon: '\uD83E\uDD1D', title: 'Collaborative Learning', desc: 'Smart group formation and peer-matching based on complementary skill sets.' },
];

export default function FeaturesSection() {
  const { t } = useLanguage();
  return (
    <>
      {/* Features Grid */}
      <section className="section-normal" id="features" style={{ paddingTop: '3rem' }}>
        <div className="container">
          <h2 className="section-title">{t('featuresSection')}</h2>
          <p className="section-subtitle">
            {t('featuresSub')}
          </p>
          <div className="row g-4">
            <div className="col-md-6 col-lg-4">
              <div className="feat-card glass">
                <div className="card-icon">🧠</div>
                <h3>{t('feat1Title')}</h3>
                <p>{t('feat1Desc')}</p>
              </div>
            </div>
            
            <div className="col-md-6 col-lg-4">
              <div className="feat-card glass">
                <div className="card-icon">⚠️</div>
                <h3>{t('feat2Title')}</h3>
                <p>{t('feat2Desc')}</p>
              </div>
            </div>
            
            <div className="col-md-6 col-lg-4">
              <div className="feat-card glass">
                <div className="card-icon">🎯</div>
                <h3>{t('feat3Title')}</h3>
                <p>{t('feat3Desc')}</p>
              </div>
            </div>
            
            <div className="col-md-6 col-lg-4">
              <div className="feat-card glass">
                <div className="card-icon">🗣️</div>
                <h3>{t('feat4Title')}</h3>
                <p>{t('feat4Desc')}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
