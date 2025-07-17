import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Language } from '../translations';

export const LanguageToggle: React.FC = () => {
  const { language, setLanguage } = useLanguage();

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'it' : 'en');
  };

  return (
    <button
      onClick={toggleLanguage}
      className="fixed top-4 right-4 z-50 bg-white border-2 border-gray-300 rounded-full px-4 py-2 text-sm font-medium hover:bg-gray-50 transition-colors"
      title={language === 'en' ? 'Switch to Italian' : 'Switch to English'}
    >
      {language === 'en' ? 'IT' : 'EN'}
    </button>
  );
};