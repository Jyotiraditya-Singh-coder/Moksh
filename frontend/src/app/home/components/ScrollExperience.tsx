'use client';

import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useLanguage } from '@/app/contexts/LanguageContext';
import BookScene, { type BookSceneHandle, PAGE_RANGES } from './BookScene';
import HeroSection from './HeroSection';

gsap.registerPlugin(ScrollTrigger);

export default function ScrollExperience() {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewportRef  = useRef<HTMLDivElement>(null);
  const bookRef      = useRef<BookSceneHandle>(null);
  const heroOverlayRef = useRef<HTMLDivElement>(null);
  const scrollIndRef   = useRef<HTMLDivElement>(null);

  const { t } = useLanguage();
  

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current!,
          start: 'top top',
          end: 'bottom bottom',
          pin: viewportRef.current!,
          scrub: 2,
          anticipatePin: 1,
          onUpdate(self) {
            bookRef.current?.setProgress(self.progress);

            const p = self.progress;

            // ── Hero text fade & scroll effect
            const heroOpacity = p <= 0.05 ? 1 - p / 0.05 : 0;
            const heroTranslateY = p <= 0.05 ? -(p / 0.05) * 50 : -50;
            
            if (heroOverlayRef.current) {
              heroOverlayRef.current.style.opacity = String(heroOpacity);
              heroOverlayRef.current.style.transform = `translateY(${heroTranslateY}px)`;
              heroOverlayRef.current.style.visibility = heroOpacity > 0 ? 'visible' : 'hidden';
            }
          },
        },
      });
    });

    return () => ctx.revert();
  }, []);

  return (
    <section ref={containerRef} className="scroll-experience" style={{ height: '700vh' }}>
      <div ref={viewportRef} className="book-viewport">
        <BookScene ref={bookRef} />

        {/* Hero overlay */}
        <div ref={heroOverlayRef} className="hero-overlay">
          <HeroSection />
        </div>

        {/* Scroll indicator */}
        <div ref={scrollIndRef} className="scroll-indicator">
          <span>{t('bookScroll')}</span>
          <div className="chevron" />
        </div>
      </div>
    </section>
  );
}
