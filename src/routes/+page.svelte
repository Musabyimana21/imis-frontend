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
      
      <div class="flex flex-col md:flex-row gap-4 justify-center mb-6">
        <a href="/report-lost" class="btn btn-primary btn-lg">
          {$t('iLostSomething')}
        </a>
        <a href="/report-found" class="btn btn-secondary btn-lg">
          {$t('iFoundSomething')}
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Items Section -->
<section class="section" style="background: var(--bg-light);">
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
<section class="section cta-section">
  <div class="container text-center">
    <h2 class="mb-4 cta-title">Get Started</h2>
    <p class="mb-6 cta-text">Join Rwandans reuniting with their lost items</p>
    
    <div class="flex flex-col md:flex-row gap-4 justify-center mb-6">
      <a href="/report-lost" class="btn btn-lg cta-btn-primary">
        Report Lost Item
      </a>
      <a href="/report-found" class="btn btn-lg cta-btn-secondary">
        Report Found Item
      </a>
    </div>
    
    <div class="flex flex-col md:flex-row gap-4 justify-center text-sm cta-features">
      <span>✓ Free to report</span>
      <span>✓ No registration required</span>
      <span>✓ Pay only when reunited</span>
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
  
  .cta-section {
    background: var(--primary);
    color: white;
  }
  
  .cta-title {
    color: white !important;
  }
  
  .cta-text {
    color: rgba(255, 255, 255, 0.9) !important;
  }
  
  .cta-btn-primary {
    background: white !important;
    color: var(--primary) !important;
    font-weight: 600;
  }
  
  .cta-btn-primary:hover {
    background: rgba(255, 255, 255, 0.9) !important;
  }
  
  .cta-btn-secondary {
    background: transparent !important;
    color: white !important;
    border: 1px solid white !important;
    font-weight: 600;
  }
  
  .cta-btn-secondary:hover {
    background: white !important;
    color: var(--primary) !important;
  }
  
  .cta-features span {
    color: rgba(255, 255, 255, 0.9) !important;
  }
</style>