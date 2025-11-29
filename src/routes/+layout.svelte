<script>
  import '../app.css';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { currentLanguage, switchLanguage, initLanguage, t } from '$lib/translations.js';
  
  let mobileMenuOpen = false;
  let lang = 'en';
  
  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }
  
  function toggleLanguage() {
    const newLang = lang === 'en' ? 'rw' : 'en';
    switchLanguage(newLang);
  }
  
  onMount(() => {
    initLanguage();
    currentLanguage.subscribe(value => {
      lang = value;
    });
  });
</script>

<!-- Navigation -->
<nav class="nav">
  <div class="nav-container">
    <a href="/" class="logo">Ishakiro</a>
    
    <ul class="nav-links">
      <li><a href="/" class:active={$page.url.pathname === '/'}>{$t('home')}</a></li>
      <li><a href="/report-lost" class:active={$page.url.pathname === '/report-lost'}>{$t('reportLost')}</a></li>
      <li><a href="/report-found" class:active={$page.url.pathname === '/report-found'}>{$t('reportFound')}</a></li>
      <li><a href="/about" class:active={$page.url.pathname === '/about'}>{$t('about')}</a></li>
      <li><a href="/contact" class:active={$page.url.pathname === '/contact'}>{$t('contact')}</a></li>
    </ul>
    
    <div class="nav-actions">
      <button on:click={toggleLanguage} class="lang-btn">
        {lang === 'en' ? 'RW' : 'EN'}
      </button>
      
      <a href="/report-lost" class="btn-cta hidden md:block">{$t('getStarted')}</a>
      
      <button class="menu-btn md:hidden" on:click={toggleMobileMenu}>
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </div>
  
  {#if mobileMenuOpen}
    <div class="mobile-menu">
      <a href="/">{$t('home')}</a>
      <a href="/report-lost">{$t('reportLost')}</a>
      <a href="/report-found">{$t('reportFound')}</a>
      <a href="/about">{$t('about')}</a>
      <a href="/contact">{$t('contact')}</a>
    </div>
  {/if}
</nav>

<!-- Main Content -->
<main style="flex: 1; display: flex; flex-direction: column;">
  <slot />
</main>

<!-- Footer -->
<footer class="footer">
  <div class="footer-content">
    <div class="footer-main">
      <div class="footer-brand">
        <h3>Ishakiro</h3>
        <p>{lang === 'en' ? 'Reuniting lost items in Rwanda' : 'Guhuriza ibintu byabuze mu Rwanda'}</p>
      </div>
      
      <div class="footer-links">
        <a href="/">{$t('home')}</a>
        <a href="/about">{$t('about')}</a>
        <a href="/contact">{$t('contact')}</a>
      </div>
      
      <div class="footer-contact">
        <p>+250780460621</p>
        <p>gaudencemusabyimana21@gmail.com</p>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>© 2025 Ishakiro. Built by MUSABYIMANA Gaudence | Made for Rwanda 🇷🇼</p>
    </div>
  </div>
</footer>

<style>
  .nav {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  
  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    text-decoration: none;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .nav-links {
    display: flex;
    gap: 2rem;
    list-style: none;
    margin: 0;
  }
  
  .nav-links a {
    color: rgba(255, 255, 255, 0.9);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
  }
  
  .nav-links a:hover,
  .nav-links a.active {
    color: white;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
  }
  
  .nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .lang-btn {
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    color: white;
    backdrop-filter: blur(10px);
  }
  
  .lang-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
  
  .btn-cta {
    padding: 0.75rem 1.5rem;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 0.5rem;
    font-weight: 600;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }
  
  .btn-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  }
  
  .menu-btn {
    display: flex;
    flex-direction: column;
    gap: 3px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
  }
  
  .menu-btn span {
    width: 20px;
    height: 2px;
    background: #374151;
    transition: all 0.2s;
  }
  
  .mobile-menu {
    display: flex;
    flex-direction: column;
    background: white;
    border-top: 1px solid #e5e7eb;
    padding: 1rem;
  }
  
  .mobile-menu a {
    padding: 0.75rem;
    color: #374151;
    text-decoration: none;
    border-radius: 0.5rem;
    transition: background 0.2s;
  }
  
  .mobile-menu a:hover {
    background: #f3f4f6;
  }
  
  .footer {
    background: #1f2937;
    color: white;
    margin-top: auto;
  }
  
  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem 1rem;
  }
  
  .footer-main {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
  }
  
  .footer-brand h3 {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: white !important;
  }
  
  .footer-brand p {
    color: #d1d5db !important;
    margin: 0;
  }
  
  .footer-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .footer-links a {
    color: #d1d5db !important;
    text-decoration: none;
    transition: color 0.2s;
  }
  
  .footer-links a:hover {
    color: white !important;
  }
  
  .footer-contact p {
    color: #d1d5db !important;
    margin: 0.25rem 0;
  }
  
  .footer-bottom {
    border-top: 1px solid #374151;
    padding-top: 1rem;
    text-align: center;
  }
  
  .footer-bottom p {
    color: #d1d5db !important;
    margin: 0;
    font-size: 0.875rem;
  }
  
  @media (max-width: 768px) {
    .nav-links {
      display: none;
    }
    
    .hidden {
      display: none;
    }
    
    .md\:block {
      display: none;
    }
    
    .md\:hidden {
      display: block;
    }
    
    .footer-main {
      grid-template-columns: 1fr;
      text-align: center;
    }
  }
  
  @media (min-width: 769px) {
    .md\:block {
      display: block;
    }
    
    .md\:hidden {
      display: none;
    }
  }
</style>