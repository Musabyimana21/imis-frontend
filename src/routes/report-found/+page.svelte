<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { currentLanguage, t } from '$lib/translations.js';
  import LocationSelector from '$lib/components/LocationSelector.svelte';
  import { env } from '$env/dynamic/public';
  
  let formData = {
    reporter_name: '',
    reporter_phone: '',
    title: '',
    description: '',
    category: 'phone',
    location: {
      province: '',
      district: '',
      sector: '',
      cell: '',
      village: '',
      isibo: ''
    }
  };
  
  let loading = false;
  let locationLoading = false;
  let selectedImage = null;
  let imagePreview = null;
  let lang = 'en';
  
  const API_URL = env.PUBLIC_API_URL || 'http://localhost:8001';
  
  // Add error handling for fetch requests
  async function fetchWithErrorHandling(url, options = {}) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP ${response.status}: ${response.statusText} - ${errorText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Fetch error:', error);
      throw error;
    }
  }
  
  const categories = [
    { value: 'phone', label: 'Phone', icon: '📱' },
    { value: 'wallet', label: 'Wallet', icon: '💼' },
    { value: 'keys', label: 'Keys', icon: '🔑' },
    { value: 'bag', label: 'Bag', icon: '🎒' },
    { value: 'documents', label: 'Documents', icon: '📄' },
    { value: 'electronics', label: 'Electronics', icon: '💻' },
    { value: 'jewelry', label: 'Jewelry', icon: '💍' },
    { value: 'other', label: 'Other', icon: '📦' }
  ];
  
  onMount(() => {
    currentLanguage.subscribe(value => {
      lang = value;
    });
  });
  
  function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('Max file size: 5MB');
        return;
      }
      
      selectedImage = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }
  
  function removeImage() {
    selectedImage = null;
    imagePreview = null;
  }
  
  function handleLocationChange(event) {
    formData.location = event.detail;
  }
  
  async function uploadImage(file) {
    // Convert to base64 since backend doesn't have upload endpoint
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.readAsDataURL(file);
    });
  }

  async function submitForm() {
    if (!formData.reporter_name || !formData.reporter_phone || !formData.title || !formData.description || !formData.location.province || !formData.location.district || !formData.location.sector || !formData.location.cell || !formData.location.village) {
      alert('Please fill in all required fields including complete location');
      return;
    }
    
    loading = true;
    try {
      let imageUrl = null;
      if (selectedImage) {
        imageUrl = await uploadImage(selectedImage);
      }
      
      const payload = {
        ...formData,
        status: 'found',
        image_url: imageUrl
      };
      
      console.log('Sending payload:', JSON.stringify(payload, null, 2));
      
      const result = await fetchWithErrorHandling(`${API_URL}/api/anonymous/report`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      
      if (result.success) {
        alert(`✅ Found item reported successfully!\n\nTracking Code: ${result.tracking_code}\n\nSave this code to track your item.`);
        goto(`/item/${result.item_id}`);
      } else {
        throw new Error(result.message || 'Failed to report item');
      }
    } catch (error) {
      console.error('Submit error:', error);
      alert('Error: ' + error.message);
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Report Found Item - Ishakiro</title>
</svelte:head>

<div class="section">
  <div class="container" style="max-width: 600px;">
    <div class="text-center mb-6">
      <h1 class="text-gradient mb-4">Report Found Item</h1>
      <p>Help reunite someone with their lost item. Your contact will be visible to owners.</p>
    </div>
      
    <div class="card">
      <form on:submit|preventDefault={submitForm} class="space-y-4">
        <h3 class="font-bold mb-4">Your Information</h3>
        
        <div class="grid grid-2 gap-4">
          <div class="form-group">
            <label class="form-label">Full Name *</label>
            <input
              type="text"
              bind:value={formData.reporter_name}
              placeholder="Your full name"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Phone Number *</label>
            <input
              type="tel"
              bind:value={formData.reporter_phone}
              placeholder="+250 788 123 456"
              class="form-input"
              required
            />
          </div>
        </div>
          
        <h3 class="font-bold mb-4">Item Details</h3>
        
        <div class="form-group">
          <label class="form-label">Item Title *</label>
          <input
            type="text"
            bind:value={formData.title}
            placeholder="e.g., Black iPhone 13 Pro"
            class="form-input"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Category *</label>
          <select bind:value={formData.category} class="form-input" required>
            {#each categories as cat}
              <option value={cat.value}>{cat.label}</option>
            {/each}
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Description *</label>
          <textarea
            bind:value={formData.description}
            placeholder="Describe the item: color, brand, model, condition, where you found it"
            class="form-input"
            rows="3"
            required
          ></textarea>
        </div>
            
        <div class="form-group">
          <label class="form-label">Upload Image (Optional)</label>
          <div class="border-2 border-dashed border-gray-300 rounded p-4 text-center">
            {#if imagePreview}
              <div class="relative">
                <img src={imagePreview} alt="Preview" class="w-full max-w-xs h-32 object-cover rounded mx-auto mb-2" />
                <button type="button" on:click={removeImage} class="btn btn-secondary text-sm">
                  Remove
                </button>
              </div>
            {:else}
              <input type="file" id="image-upload-found" accept="image/*" on:change={handleImageSelect} class="hidden" />
              <label for="image-upload-found" class="btn btn-secondary cursor-pointer">
                Choose Image
              </label>
              <p class="text-xs text-gray-500 mt-2">Max 5MB</p>
            {/if}
          </div>
        </div>
          
        <h3 class="font-bold mb-4">Location</h3>
        
        <LocationSelector
          bind:selectedLocation={formData.location}
          on:change={handleLocationChange}
        />
          
        <button
          type="submit"
          disabled={loading}
          class="btn btn-primary w-full"
        >
          {#if loading}
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Reporting...
          {:else}
            Report Found Item
          {/if}
        </button>
        
        <p class="text-center text-sm text-gray-500 mt-4">
          Free to report • Owner will contact you directly
        </p>
      </form>
    </div>
  </div>
</div>

<style>
  .w-4 {
    width: 1rem;
  }
  
  .h-4 {
    height: 1rem;
  }
  
  .w-full {
    width: 100%;
  }
  
  .flex-1 {
    flex: 1;
  }
  
  .cursor-pointer {
    cursor: pointer;
  }
  
  .hidden {
    display: none;
  }
  
  .relative {
    position: relative;
  }
  
  textarea.form-input {
    resize: vertical;
  }
</style>