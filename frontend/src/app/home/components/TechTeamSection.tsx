'use client';

import { useLanguage } from '@/app/contexts/LanguageContext';
import Image from 'next/image';

import paarthImg from '@/images/paarth.png';
import jotyImg from '@/images/joty.jpeg';
import praveenImg from '@/images/praveen.png';
import amanImg from '@/images/aman.png';

const TECH = [
  'Next.js', 'React', 'Three.js', 'GSAP', 'TypeScript',
  'TailwindCSS', 'Node.js', 'Python', 'TensorFlow', 'PostgreSQL',
];

export default function TechTeamSection() {
  const { t } = useLanguage();
  return (
    <>
      {/* Tech Stack */}
      <section className="section-normal">
        <div className="container">
          <h2 className="section-title">{t('techSection')}</h2>
          <p className="section-subtitle">{t('techSub')}</p>
          <div className="d-flex flex-wrap justify-content-center gap-3">
            {TECH.map((t) => (
              <span key={t} className="glass-card tech-badge">{t}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="section-normal">
        <div className="container">
          <h2 className="section-title">{t('teamSection')}</h2>
          <p className="section-subtitle">{t('teamSub')}</p>
          <div className="row g-4 justify-content-center">
            <div className="col-sm-6 col-lg-3">
              <div className="glass-card team-card h-100">
                <div className="team-avatar overflow-hidden">
                  <Image src={paarthImg} alt="PaarthSarthi" className="w-100 h-100 flex-shrink-0" style={{ objectFit: 'cover', objectPosition: 'top' }} />
                </div>
                <h4>{t('teamAKName')}</h4>
                <p className="role">{t('teamAKRole')}</p>
                <p>{t('teamAKDesc')}</p>
              </div>
            </div>
            <div className="col-sm-6 col-lg-3">
              <div className="glass-card team-card h-100">
                <div className="team-avatar overflow-hidden">
                  <Image src={jotyImg} alt="Jyotiraditya Singh" className="w-100 h-100 flex-shrink-0" style={{ objectFit: 'cover', objectPosition: 'top' }} />
                </div>
                <h4>{t('teamSPName')}</h4>
                <p className="role">{t('teamSPRole')}</p>
                <p>{t('teamSPDesc')}</p>
              </div>
            </div>
            <div className="col-sm-6 col-lg-3">
              <div className="glass-card team-card h-100">
                <div className="team-avatar overflow-hidden">
                  <Image src={praveenImg} alt="Praveen Kumar Sarkar" className="w-100 h-100 flex-shrink-0" style={{ objectFit: 'cover', objectPosition: 'top', transform: 'scale(1.15)', transformOrigin: 'top center' }} />
                </div>
                <h4>{t('teamMRName')}</h4>
                <p className="role">{t('teamMRRole')}</p>
                <p>{t('teamMRDesc')}</p>
              </div>
            </div>
            <div className="col-sm-6 col-lg-3">
              <div className="glass-card team-card h-100">
                <div className="team-avatar overflow-hidden">
                  <Image src={amanImg} alt="Aman Raj" className="w-100 h-100 flex-shrink-0" style={{ objectFit: 'cover', objectPosition: 'top' }} />
                </div>
                <h4>{t('teamJLName')}</h4>
                <p className="role">{t('teamJLRole')}</p>
                <p>{t('teamJLDesc')}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
