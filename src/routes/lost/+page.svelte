<script>
  import { api } from '$lib/api';
  import { goto } from '$app/navigation';
  import { t } from '$lib/stores/locale';
  import { isAuthenticated } from '$lib/stores/auth';

  let title = '';
  let description = '';
  let category = 'other';
  let locationName = '';
  let latitude = '';
  let longitude = '';
  let error = '';
  let loading = false;
  let gettingLocation = false;

  function getLocation() {
    if (navigator.geolocation) {
      gettingLocation = true;
      navigator.geolocation.getCurrentPosition(
        (position) => {
          latitude = position.coords.latitude.toString();
          longitude = position.coords.longitude.toString();
          gettingLocation = false;
        },
        (err) => {
          error = 'Unable to get location';
          gettingLocation = false;
        }
      );
    }
  }

  async function handleSubmit() {
    if (!$isAuthenticated) {
      goto('/login');
      return;
    }

    error = '';
    loading = true;

    try {
      await api.items.create({
        title,
        description,
        category,
        status: 'lost',
        location_name: locationName,
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        date_lost_found: new Date().toISOString()
      });
      
      goto('/');
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Ishakiro - Report Lost Item</title>
</svelte:head>

<div class="max-w-3xl mx-auto relative">
  <!-- Background Effects -->
  <div class="absolute inset-0 overflow-hidden pointer-events-none -z-10">
    <div class="absolute top-0 right-0 w-72 h-72 bg-red-200/30 rounded-full blur-3xl floating"></div>
    <div class="absolute bottom-0 left-0 w-72 h-72 bg-orange-200/30 rounded-full blur-3xl floating" style="animation-delay: 1s;"></div>
  </div>

  <div class="glass-card">
    <!-- Header -->
    <div class="text-center mb-10">
      <div class="inline-block p-6 bg-gradient-to-br from-red-500 to-orange-600 rounded-3xl shadow-2xl mb-6 transform hover:rotate-6 transition-transform duration-300">
        <span class="text-7xl">😢</span>
      </div>
      <h1 class="text-5xl font-black mb-4">
        <span class="bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent">
          {t('home.reportLost')}
        </span>
      </h1>
      <p class="text-xl text-gray-600">Help us find your lost item with AI-powered matching</p>
    </div>

    {#if error}
      <div class="bg-red-50 border-2 border-red-200 text-red-700 px-6 py-4 rounded-xl mb-6 animate-shake" role="alert">
        <div class="flex items-center gap-3">
          <span class="text-2xl">⚠️</span>
          <span class="font-semibold">{error}</span>
        </div>
      </div>
    {/if}

    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      <div class="grid md:grid-cols-2 gap-6">
        <div class="md:col-span-2">
          <label for="title" class="block text-sm font-bold mb-3 text-gray-700 flex items-center gap-2">
            <span class="text-xl">📝</span>
            {t('form.title')}
          </label>
          <input
            id="title"
            type="text"
            bind:value={title}
            required
            class="input-field text-lg"
            placeholder="e.g., Black iPhone 13 Pro"
          />
        </div>

        <div class="md:col-span-2">
          <label for="description" class="block text-sm font-bold mb-3 text-gray-700 flex items-center gap-2">
            <span class="text-xl">📄</span>
            {t('form.description')}
          </label>
          <textarea
            id="description"
            bind:value={description}
            required
            rows="4"
            class="input-field text-lg resize-none"
            placeholder="Describe your lost item in detail... The more details, the better the match!"
          ></textarea>
        </div>

        <div>
          <label for="category" class="block text-sm font-bold mb-3 text-gray-700 flex items-center gap-2">
            <span class="text-xl">🏷️</span>
            {t('form.category')}
          </label>
          <select id="category" bind:value={category} class="input-field text-lg">
            <option value="phone">📱 {t('categories.phone')}</option>
            <option value="wallet">💼 {t('categories.wallet')}</option>
            <option value="keys">🔑 {t('categories.keys')}</option>
            <option value="bag">🎒 {t('categories.bag')}</option>
            <option value="documents">📄 {t('categories.documents')}</option>
            <option value="electronics">💻 {t('categories.electronics')}</option>
            <option value="jewelry">💍 {t('categories.jewelry')}</option>
            <option value="other">📦 {t('categories.other')}</option>
          </select>
        </div>

        <div>
          <label for="location" class="block text-sm font-bold mb-3 text-gray-700 flex items-center gap-2">
            <span class="text-xl">📍</span>
            {t('form.location')}
          </label>
          <input
            id="location"
            type="text"
            bind:value={locationName}
            required
            class="input-field text-lg"
            placeholder="e.g., Kigali City Market"
          />
        </div>

        <div>
          <label for="latitude" class="block text-sm font-bold mb-3 text-gray-700">Latitude</label>
          <input
            id="latitude"
            type="number"
            step="any"
            bind:value={latitude}
            required
            class="input-field"
            placeholder="-1.9536"
          />
        </div>
        <div>
          <label for="longitude" class="block text-sm font-bold mb-3 text-gray-700">Longitude</label>
          <input
            id="longitude"
            type="number"
            step="any"
            bind:value={longitude}
            required
            class="input-field"
            placeholder="30.0606"
          />
        </div>
      </div>

      <button
        type="button"
        on:click={getLocation}
        disabled={gettingLocation}
        class="w-full py-4 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 text-lg"
      >
        {#if gettingLocation}
          <span class="flex items-center justify-center gap-3">
            <span class="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></span>
            Getting location...
          </span>
        {:else}
          <span class="flex items-center justify-center gap-2">
            <span class="text-2xl">📍</span>
            Use My Current Location
          </span>
        {/if}
      </button>

      <div class="flex gap-4 pt-4">
        <button
          type="submit"
          disabled={loading}
          class="btn-primary flex-1 text-lg"
        >
          {#if loading}
            <span class="flex items-center justify-center gap-3">
              <span class="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></span>
              Submitting...
            </span>
          {:else}
            <span class="flex items-center justify-center gap-2">
              <span class="text-xl">🚀</span>
              {t('form.submit')}
            </span>
          {/if}
        </button>
        <a href="/" class="btn-secondary flex-1 text-center text-lg flex items-center justify-center gap-2">
          <span class="text-xl">←</span>
          {t('form.cancel')}
        </a>
      </div>
    </form>
  </div>
</div>

<style>
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-10px); }
    75% { transform: translateX(10px); }
  }
  
  .animate-shake {
    animation: shake 0.5s ease-in-out;
  }
</style>
