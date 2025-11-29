<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { currentLanguage, t } from '$lib/translations.js';
  import { PUBLIC_API_URL } from '$env/static/public';

  let items = [];
  let loading = true;
  let filter = 'all';
  let lang = 'en';

  const API_URL = PUBLIC_API_URL || 'http://localhost:8001';

  onMount(async () => {
    try {
      const response = await fetch(`${API_URL}/api/anonymous/items`);
      if (response.ok) {
        items = await response.json();
      } else {
        console.error('Failed to load items:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Failed to load items:', error);
    } finally {
      loading = false;
    }
    
    currentLanguage.subscribe(value => {
      lang = value;
    });
  });
  
  $: filteredItems = filter === 'all' ? items : items.filter(item => item.status === filter);
</script>

<svelte:head>
  <title>Ishakiro - Reuniting Lost Items in Rwanda</title>
  <meta name="description" content="AI-powered platform to reunite lost items with their owners in Rwanda. Report lost or found items in seconds.">
</svelte:head>

<!-- Hero Section -->
<section class="hero-section">
  <div class="container">
    <div class="text-center">
      <h1 class="text-gradient mb-4">{$t('heroTitle')}</h1>
      <p class="text-xl mb-6" style="color: var(--text-light);">{$t('heroSubtitle')}</p>
      
      <div class="flex flex-col md:flex-row gap-4 justify-center mb-2">
        <a href="/report-lost" class="modern-btn modern-btn-lost">
          <span class="btn-icon">🔍</span>
          {$t('iLostSomething')}
        </a>
        <a href="/report-found" class="modern-btn modern-btn-found">
          <span class="btn-icon">✨</span>
          {$t('iFoundSomething')}
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Items Section -->
<section class="section" style="background: var(--bg-light); padding-top: 2rem;">
  <div class="container">
    <div class="text-center mb-6">
      <h2 class="text-gradient mb-4">Recent Items</h2>
    </div>
    
    <div class="flex justify-center mb-6">
      <div class="flex gap-2">
        {#each [
          { value: 'all', label: 'All' },
          { value: 'lost', label: 'Lost' },
          { value: 'found', label: 'Found' }
        ] as btn}
          <button 
            on:click={() => filter = btn.value}
            class="btn {filter === btn.value ? 'btn-primary' : 'btn-secondary'}"
          >
            {btn.label}
          </button>
        {/each}
      </div>
    </div>
    
    {#if loading}
      <div class="card text-center">
        <div class="inline-block w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p>Loading items...</p>
      </div>
    {:else if filteredItems.length === 0}
      <div class="card text-center">
        <h3 class="mb-4">No {filter === 'all' ? '' : filter} items yet</h3>
        <div class="flex gap-4 justify-center">
          <a href="/report-lost" class="btn btn-primary">Report Lost</a>
          <a href="/report-found" class="btn btn-secondary">Report Found</a>
        </div>
      </div>
    {:else}
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
        {#each filteredItems.slice(0, 12) as item}
          <a href="/item/{item.id}" style="text-decoration: none; display: block; background: white; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow: hidden; transition: all 0.3s ease; border: 1px solid #f1f5f9;" 
             onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.08)'">
            
            <!-- Image/Icon Section -->
            <div style="height: 140px; position: relative; background: {item.status === 'lost' ? 'linear-gradient(135deg, #fed7aa, #fdba74)' : 'linear-gradient(135deg, #bbf7d0, #86efac)'}; display: flex; align-items: center; justify-content: center; overflow: hidden;">
              {#if item.image_url}
                <img src="{item.image_url}" alt="{item.title}" style="width: 100%; height: 100%; object-fit: cover;" />
                <div style="position: absolute; inset: 0; background: linear-gradient(135deg, rgba(0,0,0,0.05), rgba(0,0,0,0.15));"></div>
              {:else}
                <div style="text-align: center;">
                  <div style="font-size: 50px; margin-bottom: 8px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); color: {item.status === 'lost' ? '#ea580c' : '#059669'};">
                    {#if item.category === 'phone'}📱
                    {:else if item.category === 'wallet'}💼
                    {:else if item.category === 'keys'}🔑
                    {:else if item.category === 'bag'}🎒
                    {:else if item.category === 'documents'}📄
                    {:else if item.category === 'electronics'}💻
                    {:else if item.category === 'jewelry'}💍
                    {:else}📦{/if}
                  </div>
                  <div style="background: rgba(255,255,255,0.8); padding: 4px 12px; border-radius: 12px; backdrop-filter: blur(5px); box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <p style="font-size: 12px; font-weight: 600; margin: 0; text-transform: capitalize; color: {item.status === 'lost' ? '#ea580c' : '#059669'};">{item.category}</p>
                  </div>
                </div>
              {/if}
              
              <!-- Status Badge -->
              <div style="position: absolute; top: 12px; right: 12px;">
                <span style="padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; color: white; background: {item.status === 'lost' ? '#ea580c' : '#059669'}; box-shadow: 0 2px 6px rgba(0,0,0,0.15); text-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                  {item.status.toUpperCase()}
                </span>
              </div>
            </div>
            
            <!-- Content Section -->
            <div style="padding: 16px;">
              <h3 style="font-size: 16px; font-weight: 700; color: #1e293b; margin: 0 0 8px 0; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;">{item.title}</h3>
              <p style="font-size: 13px; color: #64748b; margin: 0 0 12px 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">{item.description}</p>
              
              <div style="space-y: 6px;">
                <div style="display: flex; align-items: center; font-size: 12px; color: #64748b; margin-bottom: 6px;">
                  <span style="margin-right: 6px; font-size: 14px;">📍</span>
                  <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500;">{item.location_name.split(' → ').slice(0, 2).join(' → ')}</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: #64748b;">
                  <div style="display: flex; align-items: center;">
                    <span style="margin-right: 6px; font-size: 14px;">📅</span>
                    <span style="font-weight: 500;">{new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                  </div>
                  <div style="display: flex; align-items: center;">
                    <span style="margin-right: 6px; font-size: 14px;">👤</span>
                    <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80px; font-weight: 500;">{item.reporter_name.split(' ')[0]}</span>
                  </div>
                </div>
              </div>
            </div>
          </a>
        {/each}
      </div>
      
      {#if filteredItems.length > 12}
        <div class="text-center mt-6">
          <button class="btn btn-secondary">Load More</button>
        </div>
      {/if}
    {/if}
  </div>
</section>

<!-- Features Section -->
<section class="section">
  <div class="container">
    <div class="text-center mb-8">
      <h2 class="text-gradient mb-4">Why Ishakiro?</h2>
    </div>
    
    <div class="grid grid-2">
      {#each [
        {
          title: 'AI Matching',
          description: 'Smart algorithm finds the best matches using text and location similarity.'
        },
        {
          title: 'Mobile Money',
          description: 'Pay securely with MTN Mobile Money and Airtel Money when reunited.'
        },
        {
          title: 'Secure Chat',
          description: 'Communicate safely with item finders through our messaging system.'
        },
        {
          title: 'Made for Rwanda',
          description: 'Built for Rwandan communities with local languages and payments.'
        }
      ] as feature}
        <div class="card">
          <h3 class="font-bold mb-2">{feature.title}</h3>
          <p class="text-gray-600">{feature.description}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- CTA Section -->
<section class="cta-section-modern">
  <div class="container">
    <div class="cta-content">
      <div class="cta-header">
        <h2 class="cta-title-modern">Get Started Today</h2>
        <p class="cta-subtitle-modern">Join thousands of Rwandans reuniting with their lost items</p>
      </div>
      
      <div class="cta-buttons">
        <a href="/report-lost" class="cta-btn-modern cta-btn-lost-modern">
          <span class="cta-icon">🔍</span>
          <div class="cta-btn-content">
            <span class="cta-btn-title">Report Lost Item</span>
            <span class="cta-btn-desc">Found something? Help reunite it</span>
          </div>
        </a>
        <a href="/report-found" class="cta-btn-modern cta-btn-found-modern">
          <span class="cta-icon">✨</span>
          <div class="cta-btn-content">
            <span class="cta-btn-title">Report Found Item</span>
            <span class="cta-btn-desc">Lost something? We'll help find it</span>
          </div>
        </a>
      </div>
      
      <div class="cta-features-modern">
        <div class="cta-feature-item">
          <span class="feature-icon">✓</span>
          <span class="feature-text">Free to report</span>
        </div>
        <div class="cta-feature-item">
          <span class="feature-icon">✓</span>
          <span class="feature-text">No registration required</span>
        </div>
        <div class="cta-feature-item">
          <span class="feature-icon">✓</span>
          <span class="feature-text">Pay only when reunited</span>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  
  .w-8 {
    width: 2rem;
  }
  
  .h-8 {
    height: 2rem;
  }
  
  .cta-section-modern {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 0;
    position: relative;
    overflow: hidden;
  }
  
  .cta-section-modern::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>');
    opacity: 0.3;
  }
  
  .cta-content {
    position: relative;
    z-index: 1;
  }
  
  .cta-header {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .cta-title-modern {
    font-size: 2.5rem;
    font-weight: 800;
    color: white !important;
    margin-bottom: 1rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
  }
  
  .cta-subtitle-modern {
    font-size: 1.25rem;
    color: rgba(255, 255, 255, 0.95) !important;
    font-weight: 500;
  }
  
  .cta-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto 3rem;
  }
  
  .cta-btn-modern {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.75rem 2rem;
    background: white;
    border-radius: 16px;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  }
  
  .cta-btn-modern:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
  }
  
  .cta-icon {
    font-size: 2.5rem;
    flex-shrink: 0;
  }
  
  .cta-btn-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }
  
  .cta-btn-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  
  .cta-btn-desc {
    font-size: 0.875rem;
    opacity: 0.7;
  }
  
  .cta-btn-lost-modern {
    border-left: 5px solid #f59e0b;
  }
  
  .cta-btn-lost-modern .cta-icon {
    color: #f59e0b;
  }
  
  .cta-btn-lost-modern .cta-btn-title {
    color: #1e293b;
  }
  
  .cta-btn-lost-modern .cta-btn-desc {
    color: #64748b;
  }
  
  .cta-btn-found-modern {
    border-left: 5px solid #10b981;
  }
  
  .cta-btn-found-modern .cta-icon {
    color: #10b981;
  }
  
  .cta-btn-found-modern .cta-btn-title {
    color: #1e293b;
  }
  
  .cta-btn-found-modern .cta-btn-desc {
    color: #64748b;
  }
  
  .cta-features-modern {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    max-width: 700px;
    margin: 0 auto;
  }
  
  .cta-feature-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: white;
    font-size: 1rem;
    font-weight: 500;
  }
  
  .feature-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.875rem;
  }
  
  .feature-text {
    color: white !important;
  }
  
  @media (max-width: 768px) {
    .cta-title-modern {
      font-size: 2rem;
    }
    
    .cta-subtitle-modern {
      font-size: 1rem;
    }
    
    .cta-buttons {
      grid-template-columns: 1fr;
    }
    
    .cta-features-modern {
      flex-direction: column;
      gap: 1rem;
    }
  }
  
  .modern-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.75rem;
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: 12px;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
  
  .modern-btn-lost {
    background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
    color: white;
  }
  
  .modern-btn-lost:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
  }
  
  .modern-btn-found {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
  }
  
  .modern-btn-found:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
  }
  
  .btn-icon {
    font-size: 1.2rem;
  }
</style>