<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let selectedLocation = {
    province: '',
    district: '',
    sector: '',
    cell: '',
    village: '',
    isibo: ''
  };

  let locations = null;
  let provinces = [];
  let districts = [];
  let sectors = [];
  let cells = [];
  let villages = [];

  onMount(async () => {
    try {
      const response = await fetch('/rwanda-locations-json-master/locations.json');
      locations = await response.json();
      provinces = locations.provinces || [];
    } catch (error) {
      console.error('Failed to load locations:', error);
    }
  });

  function onProvinceChange() {
    const province = provinces.find(p => p.name === selectedLocation.province);
    districts = province ? province.districts : [];
    sectors = [];
    cells = [];
    villages = [];
    selectedLocation.district = '';
    selectedLocation.sector = '';
    selectedLocation.cell = '';
    selectedLocation.village = '';
    selectedLocation.isibo = '';
    dispatch('change', selectedLocation);
  }

  function onDistrictChange() {
    const district = districts.find(d => d.name === selectedLocation.district);
    sectors = district ? district.sectors : [];
    cells = [];
    villages = [];
    selectedLocation.sector = '';
    selectedLocation.cell = '';
    selectedLocation.village = '';
    selectedLocation.isibo = '';
    dispatch('change', selectedLocation);
  }

  function onSectorChange() {
    const sector = sectors.find(s => s.name === selectedLocation.sector);
    cells = sector ? sector.cells : [];
    villages = [];
    selectedLocation.cell = '';
    selectedLocation.village = '';
    selectedLocation.isibo = '';
    dispatch('change', selectedLocation);
  }

  function onCellChange() {
    const cell = cells.find(c => c.name === selectedLocation.cell);
    villages = cell ? cell.villages : [];
    selectedLocation.village = '';
    selectedLocation.isibo = '';
    dispatch('change', selectedLocation);
  }

  function onVillageChange() {
    selectedLocation.isibo = '';
    dispatch('change', selectedLocation);
  }

  function onIsiboChange() {
    dispatch('change', selectedLocation);
  }
</script>

<div class="space-y-4 font-sans">
  <h3 class="text-xl font-bold text-gray-900 mb-6">📍 Location (Rwanda Administrative Units)</h3>
  
  <!-- Province -->
  <div>
    <label for="province" class="block text-sm font-bold text-gray-800 mb-2">
      🏛️ Province (Intara) <span class="text-red-500">*</span>
    </label>
    <select
      id="province"
      bind:value={selectedLocation.province}
      on:change={onProvinceChange}
      class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium text-gray-800 bg-white shadow-sm"
      required
    >
      <option value="">Select Province</option>
      {#each provinces as province}
        <option value={province.name}>{province.name}</option>
      {/each}
    </select>
  </div>

  <!-- District -->
  {#if districts.length > 0}
    <div>
      <label for="district" class="block text-sm font-bold text-gray-800 mb-2">
        🏘️ District (Akarere) <span class="text-red-500">*</span>
      </label>
      <select
        id="district"
        bind:value={selectedLocation.district}
        on:change={onDistrictChange}
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium text-gray-800 bg-white shadow-sm"
        required
      >
        <option value="">Select District</option>
        {#each districts as district}
          <option value={district.name}>{district.name}</option>
        {/each}
      </select>
    </div>
  {/if}

  <!-- Sector -->
  {#if sectors.length > 0}
    <div>
      <label for="sector" class="block text-sm font-bold text-gray-800 mb-2">
        🏢 Sector (Umurenge) <span class="text-red-500">*</span>
      </label>
      <select
        id="sector"
        bind:value={selectedLocation.sector}
        on:change={onSectorChange}
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium text-gray-800 bg-white shadow-sm"
        required
      >
        <option value="">Select Sector</option>
        {#each sectors as sector}
          <option value={sector.name}>{sector.name}</option>
        {/each}
      </select>
    </div>
  {/if}

  <!-- Cell -->
  {#if cells.length > 0}
    <div>
      <label for="cell" class="block text-sm font-bold text-gray-800 mb-2">
        🏠 Cell (Akagari) <span class="text-red-500">*</span>
      </label>
      <select
        id="cell"
        bind:value={selectedLocation.cell}
        on:change={onCellChange}
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium text-gray-800 bg-white shadow-sm"
        required
      >
        <option value="">Select Cell</option>
        {#each cells as cell}
          <option value={cell.name}>{cell.name}</option>
        {/each}
      </select>
    </div>
  {/if}

  <!-- Village -->
  {#if villages.length > 0}
    <div>
      <label for="village" class="block text-sm font-bold text-gray-800 mb-2">
        🏡 Village (Umudugudu) <span class="text-red-500">*</span>
      </label>
      <select
        id="village"
        bind:value={selectedLocation.village}
        on:change={onVillageChange}
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium text-gray-800 bg-white shadow-sm"
        required
      >
        <option value="">Select Village</option>
        {#each villages as village}
          <option value={village.name}>{village.name}</option>
        {/each}
      </select>
    </div>
  {/if}

  <!-- Isibo (Optional) -->
  {#if selectedLocation.village}
    <div>
      <label for="isibo" class="block text-sm font-bold text-gray-800 mb-2">
        📍 Isibo (Optional - Specific location within village)
      </label>
      <input
        type="text"
        id="isibo"
        bind:value={selectedLocation.isibo}
        on:input={onIsiboChange}
        placeholder="e.g., Near school, Market area, etc."
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium text-gray-800 bg-white shadow-sm"
      />
    </div>
  {/if}

  <!-- Selected Location Display -->
  {#if selectedLocation.province}
    <div class="mt-6 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
      <p class="text-sm font-bold text-blue-800 mb-2">📍 Selected Location:</p>
      <p class="text-base font-semibold text-blue-900 leading-relaxed">
        {selectedLocation.province}
        {#if selectedLocation.district} → {selectedLocation.district}{/if}
        {#if selectedLocation.sector} → {selectedLocation.sector}{/if}
        {#if selectedLocation.cell} → {selectedLocation.cell}{/if}
        {#if selectedLocation.village} → {selectedLocation.village}{/if}
        {#if selectedLocation.isibo} → {selectedLocation.isibo}{/if}
      </p>
    </div>
  {/if}
</div>