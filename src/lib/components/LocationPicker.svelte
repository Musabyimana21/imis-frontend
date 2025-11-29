<script>
  import { onMount, onDestroy } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  export let latitude = -1.9536;  // Kigali center
  export let longitude = 30.0606;
  export let locationName = '';
  export let label = 'Select Location';

  const dispatch = createEventDispatcher();
  
  let map;
  let marker;
  let mapContainer;
  let showMap = false;
  let loading = false;

  // Rwanda bounds
  const RWANDA_BOUNDS = [
    [-2.84, 28.86],  // Southwest
    [-1.05, 30.90]   // Northeast
  ];

  onMount(() => {
    // Load Leaflet CSS and JS dynamically
    if (!document.getElementById('leaflet-css')) {
      const link = document.createElement('link');
      link.id = 'leaflet-css';
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(link);
    }

    if (!window.L) {
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      script.onload = () => {
        if (showMap) initMap();
      };
      document.head.appendChild(script);
    }
  });

  function toggleMap() {
    showMap = !showMap;
    if (showMap && window.L && !map) {
      setTimeout(initMap, 100);
    }
  }

  function initMap() {
    if (!mapContainer || map) return;

    map = window.L.map(mapContainer, {
      maxBounds: RWANDA_BOUNDS,
      maxBoundsViscosity: 1.0
    }).setView([latitude, longitude], 13);

    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18,
      minZoom: 8
    }).addTo(map);

    marker = window.L.marker([latitude, longitude], {
      draggable: true
    }).addTo(map);

    marker.on('dragend', async function(e) {
      const pos = marker.getLatLng();
      latitude = pos.lat;
      longitude = pos.lng;
      await reverseGeocode(latitude, longitude);
      dispatch('locationChange', { latitude, longitude, locationName });
    });

    map.on('click', async function(e) {
      latitude = e.latlng.lat;
      longitude = e.latlng.lng;
      marker.setLatLng([latitude, longitude]);
      await reverseGeocode(latitude, longitude);
      dispatch('locationChange', { latitude, longitude, locationName });
    });
  }

  async function getCurrentLocation() {
    loading = true;
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 10000
        });
      });

      latitude = position.coords.latitude;
      longitude = position.coords.longitude;

      if (map && marker) {
        map.setView([latitude, longitude], 15);
        marker.setLatLng([latitude, longitude]);
      }

      await reverseGeocode(latitude, longitude);
      dispatch('locationChange', { latitude, longitude, locationName });
    } catch (error) {
      alert('Could not get your location. Please select on map or enter manually.');
    } finally {
      loading = false;
    }
  }

  async function reverseGeocode(lat, lng) {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
      );
      const data = await response.json();
      
      if (data.address) {
        const parts = [];
        if (data.address.road) parts.push(data.address.road);
        if (data.address.suburb) parts.push(data.address.suburb);
        if (data.address.city || data.address.town) parts.push(data.address.city || data.address.town);
        if (data.address.state) parts.push(data.address.state);
        
        locationName = parts.length > 0 ? parts.join(', ') : data.display_name;
      } else {
        locationName = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
      }
    } catch (error) {
      locationName = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
    }
  }

  onDestroy(() => {
    if (map) {
      map.remove();
      map = null;
    }
  });
</script>

<div class="location-picker">
  <label class="form-label">{label} *</label>
  
  <div class="flex gap-2 mb-2">
    <input
      type="text"
      bind:value={locationName}
      placeholder="e.g., Kigali City Market, Nyabugogo"
      class="form-input flex-1"
      required
    />
    <button
      type="button"
      on:click={getCurrentLocation}
      disabled={loading}
      class="btn btn-secondary"
      title="Use my current location"
    >
      {#if loading}
        <span class="spinner"></span>
      {:else}
        📍 GPS
      {/if}
    </button>
  </div>

  <button
    type="button"
    on:click={toggleMap}
    class="btn btn-outline w-full mb-2"
  >
    {showMap ? '🗺️ Hide Map' : '🗺️ Select on Map'}
  </button>

  {#if showMap}
    <div class="map-container" bind:this={mapContainer}></div>
    <p class="text-xs text-gray-600 mt-2">
      📍 Click on map or drag marker to select location
    </p>
  {/if}

  <p class="text-xs text-gray-500 mt-1">
    Coordinates: {latitude.toFixed(4)}, {longitude.toFixed(4)}
  </p>
</div>

<style>
  .location-picker {
    margin-bottom: 1rem;
  }

  .map-container {
    width: 100%;
    height: 400px;
    border-radius: 8px;
    overflow: hidden;
    border: 2px solid #e5e7eb;
    margin-top: 0.5rem;
  }

  .flex {
    display: flex;
  }

  .gap-2 {
    gap: 0.5rem;
  }

  .mb-2 {
    margin-bottom: 0.5rem;
  }

  .mt-1 {
    margin-top: 0.25rem;
  }

  .mt-2 {
    margin-top: 0.5rem;
  }

  .flex-1 {
    flex: 1;
  }

  .w-full {
    width: 100%;
  }

  .spinner {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 2px solid currentColor;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .text-xs {
    font-size: 0.75rem;
  }

  .text-gray-500 {
    color: #6b7280;
  }

  .text-gray-600 {
    color: #4b5563;
  }
</style>
