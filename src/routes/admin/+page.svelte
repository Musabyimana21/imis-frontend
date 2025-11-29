<script>
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  import { t } from '$lib/stores/locale';
  import { goto } from '$app/navigation';
  import { isAuthenticated } from '$lib/stores/auth';

  let stats = null;
  let commissions = [];
  let users = [];
  let loading = true;
  let activeTab = 'stats';

  onMount(async () => {
    if (!$isAuthenticated) {
      goto('/login');
      return;
    }

    try {
      stats = await api.admin.getStats();
      commissions = await api.admin.getCommissions();
      users = await api.admin.getUsers();
    } catch (error) {
      console.error('Failed to load admin data:', error);
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head>
  <title>Ishakiro - Admin Dashboard</title>
</svelte:head>

<div class="max-w-7xl mx-auto relative">
  <!-- Background Effects -->
  <div class="absolute inset-0 overflow-hidden pointer-events-none -z-10">
    <div class="absolute top-0 right-0 w-96 h-96 bg-purple-200/20 rounded-full blur-3xl floating"></div>
    <div class="absolute bottom-0 left-0 w-96 h-96 bg-blue-200/20 rounded-full blur-3xl floating" style="animation-delay: 1s;"></div>
  </div>

  <!-- Header -->
  <div class="glass-card mb-10">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-5xl font-black mb-2">
          <span class="gradient-text">{t('nav.admin')} Dashboard</span>
        </h1>
        <p class="text-xl text-gray-600">Complete system overview and management</p>
      </div>
      <div class="text-7xl">👨‍💼</div>
    </div>
  </div>

  <!-- Tabs -->
  <div class="flex gap-4 mb-8 overflow-x-auto pb-2">
    {#each [
      { id: 'stats', label: 'Statistics', icon: '📊' },
      { id: 'commissions', label: 'Commissions', icon: '💰' },
      { id: 'users', label: 'Users', icon: '👥' }
    ] as tab}
      <button
        on:click={() => activeTab = tab.id}
        class="px-6 py-4 rounded-2xl font-bold transition-all duration-300 transform hover:scale-105 whitespace-nowrap {activeTab === tab.id ? 'bg-gradient-to-r from-rwanda-blue to-blue-600 text-white shadow-2xl' : 'glass-card hover:shadow-xl'}"
      >
        <span class="flex items-center gap-2 text-lg">
          <span class="text-2xl">{tab.icon}</span>
          {tab.label}
        </span>
      </button>
    {/each}
  </div>

  {#if loading}
    <div class="glass-card text-center py-20">
      <div class="inline-block w-16 h-16 border-4 border-rwanda-blue border-t-transparent rounded-full animate-spin mb-6"></div>
      <p class="text-xl text-gray-600 font-medium">Loading dashboard...</p>
    </div>
  {:else}
    {#if activeTab === 'stats' && stats}
      <div class="grid md:grid-cols-3 gap-6 mb-8">
        {#each [
          { icon: '👥', label: 'Total Users', value: stats.total_users, color: 'from-blue-500 to-cyan-500' },
          { icon: '📦', label: 'Total Items', value: stats.total_items, color: 'from-purple-500 to-pink-500' },
          { icon: '💰', label: 'Total Commissions', value: `$${stats.total_commissions.toFixed(2)}`, color: 'from-green-500 to-emerald-500' }
        ] as stat, i}
          <div class="glass-card group hover:scale-105 transition-transform duration-300" style="animation: fadeInUp 0.5s ease-out {i * 0.1}s both;">
            <div class="text-center">
              <div class="text-7xl mb-4 transform group-hover:scale-125 group-hover:rotate-12 transition-all duration-300">{stat.icon}</div>
              <div class="text-5xl font-black mb-2 bg-gradient-to-r {stat.color} bg-clip-text text-transparent">{stat.value}</div>
              <div class="text-gray-600 font-bold text-lg">{stat.label}</div>
            </div>
          </div>
        {/each}
      </div>
      
      <div class="grid md:grid-cols-3 gap-6">
        {#each [
          { icon: '😢', label: 'Lost Items', value: stats.lost_items, color: 'from-red-500 to-orange-500', bg: 'bg-red-50' },
          { icon: '🎉', label: 'Found Items', value: stats.found_items, color: 'from-green-500 to-emerald-500', bg: 'bg-green-50' },
          { icon: '✅', label: 'Recovered Items', value: stats.recovered_items, color: 'from-blue-500 to-cyan-500', bg: 'bg-blue-50' }
        ] as stat, i}
          <div class="glass-card {stat.bg} border-2 border-white/50" style="animation: fadeInUp 0.5s ease-out {(i + 3) * 0.1}s both;">
            <div class="text-center">
              <div class="text-6xl mb-4">{stat.icon}</div>
              <div class="text-4xl font-black mb-2 bg-gradient-to-r {stat.color} bg-clip-text text-transparent">{stat.value}</div>
              <div class="text-gray-700 font-bold">{stat.label}</div>
            </div>
          </div>
        {/each}
      </div>
    {/if}

    {#if activeTab === 'commissions'}
      <div class="glass-card">
        <h2 class="text-3xl font-black mb-6 flex items-center gap-3">
          <span class="text-4xl">💰</span>
          Commission History
        </h2>
        {#if commissions.length === 0}
          <div class="text-center py-12">
            <div class="text-8xl mb-4">📊</div>
            <p class="text-xl text-gray-600">No commissions yet</p>
          </div>
        {:else}
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b-2 border-gray-200">
                  <th class="text-left py-4 px-4 font-black">ID</th>
                  <th class="text-left py-4 px-4 font-black">Item ID</th>
                  <th class="text-left py-4 px-4 font-black">Amount</th>
                  <th class="text-left py-4 px-4 font-black">Rate</th>
                  <th class="text-left py-4 px-4 font-black">Status</th>
                  <th class="text-left py-4 px-4 font-black">Date</th>
                </tr>
              </thead>
              <tbody>
                {#each commissions as commission}
                  <tr class="border-b border-gray-100 hover:bg-white/50 transition-colors">
                    <td class="py-4 px-4 font-mono">#{commission.id}</td>
                    <td class="py-4 px-4 font-mono">#{commission.item_id}</td>
                    <td class="py-4 px-4 font-bold text-green-600">${commission.amount.toFixed(2)}</td>
                    <td class="py-4 px-4">{(commission.rate * 100).toFixed(0)}%</td>
                    <td class="py-4 px-4">
                      <span class="px-3 py-1 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-full text-xs font-bold">
                        {commission.status}
                      </span>
                    </td>
                    <td class="py-4 px-4 text-gray-600">{new Date(commission.created_at).toLocaleDateString()}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/if}
      </div>
    {/if}

    {#if activeTab === 'users'}
      <div class="glass-card">
        <h2 class="text-3xl font-black mb-6 flex items-center gap-3">
          <span class="text-4xl">👥</span>
          User Management
        </h2>
        {#if users.length === 0}
          <div class="text-center py-12">
            <div class="text-8xl mb-4">👤</div>
            <p class="text-xl text-gray-600">No users yet</p>
          </div>
        {:else}
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b-2 border-gray-200">
                  <th class="text-left py-4 px-4 font-black">ID</th>
                  <th class="text-left py-4 px-4 font-black">Name</th>
                  <th class="text-left py-4 px-4 font-black">Email</th>
                  <th class="text-left py-4 px-4 font-black">Role</th>
                  <th class="text-left py-4 px-4 font-black">Joined</th>
                </tr>
              </thead>
              <tbody>
                {#each users as user}
                  <tr class="border-b border-gray-100 hover:bg-white/50 transition-colors">
                    <td class="py-4 px-4 font-mono">#{user.id}</td>
                    <td class="py-4 px-4 font-semibold">{user.full_name}</td>
                    <td class="py-4 px-4 text-gray-600">{user.email}</td>
                    <td class="py-4 px-4">
                      <span class="px-3 py-1 bg-gradient-to-r {user.role === 'admin' ? 'from-purple-500 to-pink-500' : 'from-blue-500 to-cyan-500'} text-white rounded-full text-xs font-bold uppercase">
                        {user.role}
                      </span>
                    </td>
                    <td class="py-4 px-4 text-gray-600">{new Date(user.created_at).toLocaleDateString()}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/if}
      </div>
    {/if}
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
