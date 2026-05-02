'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Central dictionary for all translatable strings in the app
export const englishDictionary = {
  // Hero section
  heroTitle: "EduNex AI",
  heroSubtitle: "The Future of Learning",
  heroDesc: "Experience the next evolution in education with our intelligent, adaptive platform designed to unlock every learner's full potential.",
  heroStarted: "Get Started",
  heroDemo: "Watch Demo",

  // NavBar
  navLog: "Log In",
  navSign: "SignUp",
  navHome: "Home",
  navFeatures: "Features",
  navTech: "Technology",
  navTeam: "Team",
  navContact: "Contact",

  // Sections
  featuresSection: "Key Features",
  featuresSub: "Discover how AI transforms the learning experience.",
  techSection: "Built with Modern Tech",
  techSub: "Powered by the latest tools to ensure performance and reliability.",
  teamSection: "Our Team",
  teamSub: "A world-class team passionate about transforming education with AI.",

  // Features Cards
  feat1Title: "AI Daily Learning Challenges",
  feat1Desc: "Personalized daily challenges powered by AI that adapt to your pace and mastery level.",
  feat2Title: "Dropout Risk Prediction",
  feat2Desc: "Proactive risk scoring identifies at-risk students early so educators can intervene in time.",
  feat3Title: "Skill Gap Analyzer",
  feat3Desc: "Radar-based skill mapping pinpoints exactly where learners need targeted practice.",
  feat4Title: "Multilingual Voice Tutor",
  feat4Desc: "Speak and learn in 50+ languages with a real-time AI voice coach by your side.",

  // About Section
  aboutSection: "About the Platform",
  aboutText: "EduNex AI is a next-generation education platform that harnesses artificial intelligence to deliver deeply personalized learning experiences. From adaptive challenges to predictive analytics, we empower institutions and learners alike.",

  // Book Pages 
  bookCoverSub: "The Future of Learning",
  bookPage0Text: "Choose Your Language",
  bookPage1Text: "Select Your Path",
  bookStudent: "Student",
  bookStudentSub: "K-12 & University",
  bookJob: "Job Professional",
  bookJobSub: "Upskilling & Career Transition",

  // Book Dynamic Paths
  bookHomeworkTitle: "Homework AI Helper",
  bookInterviewTitle: "Interview Preparation",
  bookSkillGap: "Skill Gap Analyzer",
  bookCareerMap: "Career Strategy Roadmap",
  bookScroll: "Scroll to explore",
  bookAwaiting: "Awaiting Selection...",
  bookPathInstruct: "Select a path on the previous page",

  // Radar Labels
  bookMath: "Math",
  bookScience: "Science",
  bookEnglish: "English",
  bookHistory: "History",
  bookArt: "Art",
  bookCode: "Code",

  // CTA
  ctaTitle: "Ready to Transform Learning?",
  ctaSub: "Join thousands of students and educators already using the future of education.",

  // Footer
  footerDesc: "Personalized AI Education Intelligence — shaping the future of learning.",
  footerProduct: "Product",
  footerPricing: "Pricing",
  footerIntegrations: "Integrations",
  footerCompany: "Company",
  footerAbout: "About",
  footerBlog: "Blog",
  footerCareers: "Careers",
  footerStayUpdated: "Stay Updated",
  footerSubscribe: "Subscribe for product updates and AI education insights.",
  footerJoin: "Join",
  footerEmailPlaceholder: "your@email.com",
  footerRights: "© 2024 EduNex AI. All rights reserved.",

  // Misc
  translatingSmall: "Translating...",

  // Team
  teamAKName: "PaarthSarthi",
  teamAKRole: "Team Lead",
  teamAKDesc: "NASA 3rd runner-up all over India.",
  teamSPName: "Jyotiraditya Singh",
  teamSPRole: "Full Stack Developer",
  teamSPDesc: "16+ GitHub repos, and 5+ live-project builds.",
  teamMRName: "Praveen Kumar Sarkar",
  teamMRRole: "Backend Developer",
  teamMRDesc: "Core backend architect with expertise in scalable systems and AI integration.",
  teamJLName: "Aman Raj",
  teamJLRole: "Frontend Developer",
  teamJLDesc: "Creative frontend developer specializing in UI design."
};

type Dictionary = typeof englishDictionary;

interface LanguageContextProps {
  lang: string;
  setLang: (lang: string) => void;
  // A function that gets a translated string by its key
  t: (key: keyof Dictionary) => string;
  isTranslating: boolean;
}

const LanguageContext = createContext<LanguageContextProps | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState('en');
  const [translations, setTranslations] = useState<Record<string, string>>(englishDictionary);
  const [isTranslating, setIsTranslating] = useState(false);

  // Expose the setter and trigger network fetch
  const setLang = async (newLang: string) => {
    if (newLang === lang) return;
    setLangState(newLang);

    if (newLang === 'en') {
      setTranslations(englishDictionary);
      return;
    }

    setIsTranslating(true);
    try {
      const res = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          targetLang: newLang,
          texts: englishDictionary
        })
      });
      const data = await res.json();
      if (data.translations) {
        setTranslations(data.translations);
      } else {
        console.error("Translation API returned an error:", data.error);
      }
    } catch (e) {
      console.error("Failed to map translation dictionary:", e);
    } finally {
      setIsTranslating(false);
    }
  };

  // Helper method used by all components
  const t = (key: keyof Dictionary): string => {
    return translations[key] || englishDictionary[key];
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t, isTranslating }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
