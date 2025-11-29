import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { translations } from '../i18n/translations';

const storedLocale = browser ? localStorage.getItem('locale') || 'en' : 'en';

export const locale = writable(storedLocale);

locale.subscribe(value => {
  if (browser) {
    localStorage.setItem('locale', value);
  }
});

export function t(key) {
  let currentLocale = 'en';
  locale.subscribe(value => currentLocale = value)();
  
  const keys = key.split('.');
  let translation = translations[currentLocale];
  
  for (const k of keys) {
    translation = translation?.[k];
  }
  
  return translation || key;
}
