<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { api } from '$lib/api';
  import { isAuthenticated } from '$lib/stores/auth';

  let item = null;
  let matches = [];
  let loading = true;
  let messageContent = '';
  let showMessageForm = false;
  let sendingMessage = false;

  const categoryIcons = {
    phone: '📱', wallet: '💼', keys: '🔑', bag: '🎒',
    documents: '📄', electronics: '💻', jewelry: '💍', other: '📦'
  };

  const statusConfig = {
    lost: { color: 'from-red-500 to-red-700', bg: 'bg-red-50' },
    found: { color: 'from-green-500 to-green-700', bg: 'bg-green-50' },
    matched: { color: 'from-yellow-500 to-yellow-700', bg: 'bg-yellow-50' },
    recovered: { color: 'from-blue-500 to-blue-700', bg: 'bg-blue-50' }
  };

  onMount(async () => {
    const itemId = $page.params.id;
    
    try {
      item = await api.items.getOne(itemId);
      if ($isAuthenticated) {
        matches = await api.items.getMatches(itemId);
      }
    } catch (error) {
      console.error('Failed to load item:', error);
    } finally {
      loading = false;
    }
  });

  async function sendMessage(receiverId) {
    if (!messageContent.trim()) return;
    sendingMessage = true;

    try {
      await api.messages.send({
        receiver_id: receiverId,
        item_id: item.id,
        content: messageContent
      });
      messageContent = '';
      showMessageForm = false;
      alert('✅ Message sent successfully!');
    } catch (error) {
      alert('❌ Failed to send message: ' + error.message);
    } finally {
      sendingMessage = false;
    }
  }

  $: config = item ? statusConfig[item.status] || statusConfig.lost : statusConfig.lost;
</script>

<svelte:head>
  <title>Ishakiro - {item?.title || 'Item Details'}</title>
</svelte:head>

<div class="max-w-6xl mx-auto relative">
  <div class="absolute inset-0 overflow-hidden pointer-events-none -z-10">
    <div class="absolute top-0 right-0 w-96 h-96 bg-blue-200/20 rounded-full blur-3xl floating"></div>
    <div class="absolute bottom-0 left-0 w-96 h-96 bg-purple-200/20 rounded-full blur-3xl floating" style="animation-delay: 1s;"></div>
  </div>

  {#if loading}
    <div class="glass-card text-center py-20">
      <div class="inline-block w-16 h-16 border-4 border-rwanda-blue border-t-transparent rounded-full animate-spin mb-6"></div>
      <p class="text-xl text-gray-600 font-medium">Loading item details...</p>
    </div>
  {:else if item}
    <div class="glass-card mb-8">
      <div class="grid md:grid-cols-2 gap-8">
        <div class="relative {config.bg} rounded-3xl p-12 flex items-center justify-center overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br {config.color} opacity-10"></div>
          <div class="text-9xl relative z-10 transform hover:scale-110 transition-transform duration-300">
            {categoryIcons[item.category] || '📦'}
          </div>
        </div>
        
        <div class="space-y-6">
          <div>
            <div class="inline-block px-4 py-2 bg-gradient-to-r {config.color} text-white rounded-full text-sm font-black uppercase mb-4">
              {item.status}
            </div>
            <h1 class="text-4xl font-black mb-4 gradient-text">{item.title}</h1>
          </div>

          <div class="space-y-4">
            <div class="flex items-center gap-3 p-3 bg-white/50 rounded-xl">
              <span class="text-2xl">🏷️</span>
              <div>
                <div class="text-xs text-gray-500 font-semibold">Category</div>
                <div class="font-bold capitalize">{item.category}</div>
              </div>
            </div>

            <div class="flex items-center gap-3 p-3 bg-white/50 rounded-xl">
              <span class="text-2xl">📍</span>
              <div>
                <div class="text-xs text-gray-500 font-semibold">Location</div>
                <div class="font-bold">{item.location_name}</div>
                <div class="text-xs text-gray-500">{item.latitude.toFixed(4)}, {item.longitude.toFixed(4)}</div>
              </div>
            </div>

            <div class="flex items-center gap-3 p-3 bg-white/50 rounded-xl">
              <span class="text-2xl">📅</span>
              <div>
                <div class="text-xs text-gray-500 font-semibold">Posted</div>
                <div class="font-bold">{new Date(item.created_at).toLocaleDateString()}</div>
              </div>
            </div>
          </div>
          
          <div class="p-4 bg-white/50 rounded-xl">
            <h2 class="font-black text-lg mb-3 flex items-center gap-2">
              <span class="text-xl">📄</span>
              Description
            </h2>
            <p class="text-gray-700 leading-relaxed">{item.description}</p>
          </div>

          {#if $isAuthenticated}
            <button
              on:click={() => showMessageForm = !showMessageForm}
              class="btn-primary w-full text-lg"
            >
              <span class="flex items-center justify-center gap-2">
                <span class="text-xl">💬</span>
                Contact Owner
              </span>
            </button>

            {#if showMessageForm}
              <div class="p-4 bg-white/50 rounded-xl space-y-3">
                <textarea
                  bind:value={messageContent}
                  placeholder="Type your message here..."
                  rows="4"
                  class="input-field"
                ></textarea>
                <button
                  on:click={() => sendMessage(item.user_id)}
                  disabled={sendingMessage || !messageContent.trim()}
                  class="btn-secondary w-full"
                >
                  {#if sendingMessage}
                    <span class="flex items-center justify-center gap-3">
                      <span class="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></span>
                      Sending...
                    </span>
                  {:else}
                    <span class="flex items-center justify-center gap-2">
                      <span class="text-xl">📤</span>
                      Send Message
                    </span>
                  {/if}
                </button>
              </div>
            {/if}
          {:else}
            <a href="/login" class="btn-primary w-full text-center text-lg">
              <span class="flex items-center justify-center gap-2">
                <span class="text-xl">🔐</span>
                Login to Contact Owner
              </span>
            </a>
          {/if}
        </div>
      </div>
    </div>

    {#if matches.length > 0}
      <div class="glass-card">
        <h2 class="text-3xl font-black mb-6 flex items-center gap-3">
          <span class="text-4xl">🎯</span>
          <span class="gradient-text">AI-Matched Items ({matches.length})</span>
        </h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each matches as match}
            <a href={`/items/${match.matched_item.id}`} class="glass-card hover:scale-105 transition-transform duration-300">
              <div class="text-center mb-4">
                <div class="text-6xl mb-3">{categoryIcons[match.matched_item.category] || '📦'}</div>
                <h3 class="font-black text-lg mb-2">{match.matched_item.title}</h3>
                <p class="text-sm text-gray-600 mb-3">{match.matched_item.location_name}</p>
              </div>
              <div class="flex gap-2">
                <div class="flex-1 text-center p-2 bg-green-50 rounded-lg">
                  <div class="text-2xl font-black text-green-600">{(match.similarity_score * 100).toFixed(0)}%</div>
                  <div class="text-xs text-gray-600">Match</div>
                </div>
                <div class="flex-1 text-center p-2 bg-blue-50 rounded-lg">
                  <div class="text-2xl font-black text-blue-600">{match.distance_km.toFixed(1)}</div>
                  <div class="text-xs text-gray-600">km away</div>
                </div>
              </div>
            </a>
          {/each}
        </div>
      </div>
    {:else if $isAuthenticated}
      <div class="glass-card text-center py-12">
        <div class="text-8xl mb-4">🔍</div>
        <p class="text-xl text-gray-700 font-bold mb-2">No matches found yet</p>
        <p class="text-gray-600">Our AI will notify you when similar items are reported!</p>
      </div>
    {/if}
  {:else}
    <div class="glass-card text-center py-20">
      <div class="text-8xl mb-6">❌</div>
      <p class="text-2xl text-gray-700 font-bold mb-4">Item not found</p>
      <a href="/" class="btn-primary inline-block">Back to Home</a>
    </div>
  {/if}
</div>
