<script>
  let formData = {
    name: '',
    email: '',
    subject: '',
    message: ''
  };
  
  let loading = false;
  
  async function submitForm() {
    if (!formData.name || !formData.email || !formData.subject || !formData.message) {
      alert('Please fill in all fields');
      return;
    }
    
    loading = true;
    
    // Simulate form submission
    setTimeout(() => {
      alert('✅ Message sent successfully! We will get back to you within 24 hours.');
      formData = { name: '', email: '', subject: '', message: '' };
      loading = false;
    }, 1000);
  }
</script>

<svelte:head>
  <title>Contact Us - Ishakiro</title>
</svelte:head>

<div class="section">
  <div class="container">
    <div class="text-center mb-8">
      <h1 class="text-gradient mb-4">Contact Us</h1>
      <p>Have questions? We're here to help.</p>
    </div>

    <div class="grid grid-2">
      <!-- Contact Form -->
      <div class="card">
        <h2 class="mb-4">Send Message</h2>
        <form on:submit|preventDefault={submitForm} class="space-y-4">
          <div class="form-group">
            <label class="form-label">Full Name *</label>
            <input
              type="text"
              bind:value={formData.name}
              placeholder="Your name"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Email *</label>
            <input
              type="email"
              bind:value={formData.email}
              placeholder="your.email@example.com"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Subject *</label>
            <input
              type="text"
              bind:value={formData.subject}
              placeholder="What is this about?"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Message *</label>
            <textarea
              bind:value={formData.message}
              placeholder="How can we help?"
              class="form-input"
              rows="4"
              required
            ></textarea>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            class="btn btn-primary w-full"
          >
            {#if loading}
              <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Sending...
            {:else}
              Send Message
            {/if}
          </button>
        </form>
      </div>

      <!-- Contact Information -->
      <div class="space-y-4">
        <div class="card">
          <h3 class="mb-4">Contact Info</h3>
          <div class="space-y-3">
            <div>
              <div class="font-semibold">Phone</div>
              <div class="text-gray-600">+250780460621</div>
            </div>
            <div>
              <div class="font-semibold">Email</div>
              <div class="text-gray-600">gaudencemusabyimana21@gmail.com</div>
            </div>
            <div>
              <div class="font-semibold">Location</div>
              <div class="text-gray-600">Kigali, Rwanda</div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="mb-4">Developer Info</h3>
          <div class="space-y-2 text-sm">
            <div>
              <div class="font-semibold">Developer</div>
              <div class="text-gray-600">MUSABYIMANA Gaudence</div>
            </div>
            <div>
              <div class="font-semibold">Contact</div>
              <div class="text-gray-600">+250780460621</div>
            </div>
            <div>
              <div class="font-semibold">Email</div>
              <div class="text-gray-600">gaudencemusabyimana21@gmail.com</div>
            </div>
          </div>
          <div class="mt-3 p-2 bg-green-50 rounded text-sm text-green-700">
            System available 24/7
          </div>
        </div>

        <div class="card">
          <h3 class="mb-4">Quick Links</h3>
          <div class="space-y-2">
            <a href="/about" class="block p-2 rounded hover:bg-gray-50">
              How it works
            </a>
            <a href="/report-lost" class="block p-2 rounded hover:bg-gray-50">
              Report lost item
            </a>
            <a href="/report-found" class="block p-2 rounded hover:bg-gray-50">
              Report found item
            </a>
          </div>
        </div>
      </div>
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
  
  textarea.form-input {
    resize: vertical;
  }
</style>