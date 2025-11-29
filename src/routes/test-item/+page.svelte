<script>
  import { onMount } from 'svelte';

  let items = [];
  let loading = true;
  let error = null;

  const API_URL = 'http://localhost:8001';

  onMount(async () => {
    try {
      const res = await fetch(`${API_URL}/anonymous/items`);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      items = await res.json();
    } catch (err) {
      error = err.message;
      console.error('Failed to load items:', err);
    } finally {
      loading = false;
    }
  });
</script>

<div class="max-w-4xl mx-auto p-6">
  <h1 class="text-3xl font-bold mb-6">🧪 Test Items Page</h1>
  
  {#if loading}
    <div class="text-center py-8">
      <div class="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-2">Loading items...</p>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 rounded-lg p-4">
      <h2 class="text-red-800 font-bold">❌ Error</h2>
      <p class="text-red-700">{error}</p>
    </div>
  {:else if items.length === 0}
    <div class="text-center py-8">
      <p class="text-gray-500">No items found</p>
    </div>
  {:else}
    <div class="space-y-4">
      <p class="text-green-600 font-bold">✅ Found {items.length} items</p>
      {#each items as item}
        <div class="border rounded-lg p-4 bg-white shadow">
          <h3 class="font-bold text-lg">
            <a href="/item/{item.id}" class="text-blue-600 hover:underline">
              {item.title}
            </a>
          </h3>
          <p class="text-gray-600">{item.description}</p>
          <div class="mt-2 text-sm text-gray-500">
            <span class="font-medium">Status:</span> {item.status} |
            <span class="font-medium">Location:</span> {item.location_name} |
            <span class="font-medium">ID:</span> {item.id}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>