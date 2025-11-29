<script>
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import { t } from '$lib/stores/locale';
  import { goto } from '$app/navigation';
  import { isAuthenticated } from '$lib/stores/auth';

  let messages = [];
  let loading = true;

  onMount(async () => {
    if (!$isAuthenticated) {
      goto('/login');
      return;
    }

    try {
      messages = await api.messages.getAll();
    } catch (error) {
      console.error('Failed to load messages:', error);
    } finally {
      loading = false;
    }
  });

  async function markAsRead(messageId) {
    try {
      await api.messages.markRead(messageId);
      messages = messages.map(m => 
        m.id === messageId ? { ...m, is_read: true } : m
      );
    } catch (error) {
      console.error('Failed to mark as read:', error);
    }
  }
</script>

<svelte:head>
  <title>Ishakiro - Messages</title>
</svelte:head>

<div class="max-w-4xl mx-auto relative">
  <!-- Background Effects -->
  <div class="absolute inset-0 overflow-hidden pointer-events-none -z-10">
    <div class="absolute top-0 left-0 w-72 h-72 bg-blue-200/20 rounded-full blur-3xl floating"></div>
    <div class="absolute bottom-0 right-0 w-72 h-72 bg-purple-200/20 rounded-full blur-3xl floating" style="animation-delay: 1s;"></div>
  </div>

  <!-- Header -->
  <div class="glass-card mb-10">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-5xl font-black mb-2">
          <span class="gradient-text">{t('nav.messages')}</span>
        </h1>
        <p class="text-xl text-gray-600">Your conversations and notifications</p>
      </div>
      <div class="relative">
        <div class="text-7xl">💬</div>
        {#if messages.filter(m => !m.is_read).length > 0}
          <div class="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-red-500 to-orange-500 rounded-full flex items-center justify-center text-white font-black text-sm shadow-lg animate-pulse">
            {messages.filter(m => !m.is_read).length}
          </div>
        {/if}
      </div>
    </div>
  </div>

  {#if loading}
    <div class="glass-card text-center py-20">
      <div class="inline-block w-16 h-16 border-4 border-rwanda-blue border-t-transparent rounded-full animate-spin mb-6"></div>
      <p class="text-xl text-gray-600 font-medium">Loading messages...</p>
    </div>
  {:else if messages.length === 0}
    <div class="glass-card text-center py-20">
      <div class="text-8xl mb-6">📭</div>
      <p class="text-2xl text-gray-700 font-bold mb-4">No messages yet</p>
      <p class="text-gray-600 mb-8">Start connecting with people to reunite lost items!</p>
      <a href="/" class="btn-primary inline-block">Browse Items</a>
    </div>
  {:else}
    <div class="space-y-4">
      {#each messages as message, i}
        <div 
          class="glass-card {message.is_read ? 'bg-white/60' : 'bg-blue-50/80 border-2 border-blue-200'} hover:scale-[1.02] transition-all duration-300"
          style="animation: fadeInUp 0.5s ease-out {i * 0.05}s both;"
        >
          <div class="flex justify-between items-start mb-4">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-gradient-to-br from-rwanda-blue to-rwanda-green rounded-full flex items-center justify-center text-2xl shadow-lg">
                {message.sender_id === message.receiver_id ? '👤' : '👥'}
              </div>
              <div>
                <p class="font-black text-lg text-gray-800">
                  {message.sender_id === message.receiver_id ? 'You' : `User #${message.sender_id}`}
                </p>
                <p class="text-sm text-gray-500 flex items-center gap-2">
                  <span>🕒</span>
                  {new Date(message.created_at).toLocaleString()}
                </p>
              </div>
            </div>
            {#if !message.is_read}
              <button
                on:click={() => markAsRead(message.id)}
                class="px-4 py-2 bg-gradient-to-r from-rwanda-blue to-blue-600 text-white rounded-xl font-bold text-sm hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-300"
              >
                ✓ Mark as read
              </button>
            {/if}
          </div>
          
          <div class="bg-white/50 rounded-xl p-4 border border-gray-200">
            <p class="text-gray-700 leading-relaxed">{message.content}</p>
          </div>
          
          {#if !message.is_read}
            <div class="mt-3 flex items-center gap-2 text-sm font-bold text-blue-600">
              <span class="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></span>
              New message
            </div>
          {/if}
        </div>
      {/each}
    </div>
    
    <!-- Stats -->
    <div class="glass-card mt-8">
      <div class="grid md:grid-cols-3 gap-6 text-center">
        <div>
          <div class="text-4xl mb-2">📨</div>
          <div class="text-3xl font-black text-rwanda-blue">{messages.length}</div>
          <div class="text-gray-600 font-semibold">Total Messages</div>
        </div>
        <div>
          <div class="text-4xl mb-2">✉️</div>
          <div class="text-3xl font-black text-blue-600">{messages.filter(m => !m.is_read).length}</div>
          <div class="text-gray-600 font-semibold">Unread</div>
        </div>
        <div>
          <div class="text-4xl mb-2">✅</div>
          <div class="text-3xl font-black text-green-600">{messages.filter(m => m.is_read).length}</div>
          <div class="text-gray-600 font-semibold">Read</div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
