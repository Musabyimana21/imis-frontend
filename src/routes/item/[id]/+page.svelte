<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { env } from '$env/dynamic/public';

  export let data;
  let item = null;
  let loading = true;
  let showPayment = false;
  let paymentMethod = 'MTN_MOMO';
  let payerPhone = '';
  let currentImageIndex = 0;
  let pricingInfo = null;

  const API_URL = env.PUBLIC_API_URL || 'http://localhost:8001';

  onMount(async () => {
    const itemId = data?.props?.id || $page.params.id;
    console.log('Loading item with ID:', itemId);
    try {
      const res = await fetch(`${API_URL}/api/anonymous/items`);
      const items = await res.json();
      item = items.find(i => i.id == itemId);
      if (item) {
        console.log('Item loaded:', item);
        console.log('Image URL:', item.image_url);
        
        // Load pricing info for this category
        try {
          const pricingRes = await fetch(`${API_URL}/api/anonymous/pricing/${item.category}`);
          if (pricingRes.ok) {
            pricingInfo = await pricingRes.json();
            console.log('Pricing info:', pricingInfo);
          }
        } catch (error) {
          console.error('Failed to load pricing:', error);
        }
      } else {
        console.log('Item not found');
      }
    } catch (error) {
      console.error('Failed to load:', error);
    } finally {
      loading = false;
    }
  });

  function getCategoryIcon(category) {
    const icons = {
      'phone': '📱', 'wallet': '💼', 'keys': '🔑', 'bag': '🎒',
      'documents': '📄', 'electronics': '💻', 'jewelry': '💍', 'other': '📦'
    };
    return icons[category] || '📦';
  }
  
  async function processPayment() {
    if (!payerPhone.trim()) {
      alert('Please enter your phone number');
      return;
    }
    
    try {
      const response = await fetch(`${API_URL}/api/anonymous/payment/initiate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          item_id: item.id,
          payer_phone: payerPhone,
          payment_method: "mtn_momo"
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        
        if (result.success && result.transaction_id) {
          alert(`Payment initiated! ${result.message}`);
          showPayment = false;
          
          // Check payment status after a few seconds
          setTimeout(async () => {
            try {
              const statusResponse = await fetch(`${API_URL}/api/anonymous/payment/status/${result.transaction_id}`);
              if (statusResponse.ok) {
                const statusResult = await statusResponse.json();
                if (statusResult.success && statusResult.contact_unlocked) {
                  alert(`Payment successful! Contact: ${statusResult.reporter_name} - ${statusResult.reporter_phone}`);
                  // Reload the page to show unlocked contact
                  location.reload();
                }
              }
            } catch (error) {
              console.error('Status check error:', error);
            }
          }, 10000); // Check after 10 seconds
        } else {
          let errorMsg = result.error || 'Payment failed';
          if (result.alternatives) {
            errorMsg += '\n\nAlternative Payment Methods:';
            if (result.alternatives.airtel_money) errorMsg += '\n• Airtel Money: ' + result.alternatives.airtel_money;
            if (result.alternatives.bank_transfer) errorMsg += '\n• Bank Transfer: ' + result.alternatives.bank_transfer;
            if (result.alternatives.cash_payment) errorMsg += '\n• Cash Payment: ' + result.alternatives.cash_payment;
            if (result.support_contact) errorMsg += '\n\nSupport: ' + result.support_contact;
          }
          alert(errorMsg);
          showPayment = false;
        }
        
      } else {
        const error = await response.text();
        alert(`Payment failed: ${error}`);
        showPayment = false;
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert('Payment failed. Please try again.');
    }
  }
</script>

<div style="min-height: 100vh; background: #f8fafc; padding: 20px;">
  {#if loading}
    <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
      <div style="text-align: center;">
        <div style="width: 50px; height: 50px; border: 4px solid #3b82f6; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px;"></div>
        <p style="color: #6b7280; font-size: 18px;">Loading item...</p>
      </div>
    </div>
  {:else if item}
    <div style="max-width: 800px; margin: 0 auto;">
      
      <!-- Back Button -->
      <div style="margin-bottom: 30px;">
        <a href="/" style="color: #3b82f6; text-decoration: none; font-weight: 600; font-size: 16px;">
          ← Back to Items
        </a>
      </div>

      <!-- Main Card -->
      <div style="background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden;">
        
        <!-- Image Section -->
        <div style="height: 400px; position: relative; background: {item.status === 'lost' ? 'linear-gradient(135deg, #fed7aa, #fdba74)' : 'linear-gradient(135deg, #bbf7d0, #86efac)'}; display: flex; align-items: center; justify-content: center;">
          {#if item.image_url && item.image_url.trim() !== ''}
            <img 
              src="{item.image_url}" 
              alt="{item.title}" 
              style="width: 100%; height: 100%; object-fit: cover;"
              on:error={() => console.log('Image failed to load:', item.image_url)}
            />
          {:else}
            <div style="text-align: center;">
              <div style="font-size: 120px; margin-bottom: 20px; color: {item.status === 'lost' ? '#ea580c' : '#059669'}; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));">{getCategoryIcon(item.category)}</div>
              <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 15px; backdrop-filter: blur(5px); box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <p style="font-size: 24px; font-weight: bold; margin: 0 0 10px 0; color: {item.status === 'lost' ? '#ea580c' : '#059669'};">{item.category.charAt(0).toUpperCase() + item.category.slice(1)}</p>
                <p style="font-size: 16px; margin: 0; color: #64748b;">No photo provided</p>
              </div>
            </div>
          {/if}
          
          <!-- Status Badge -->
          <div style="position: absolute; top: 20px; right: 20px;">
            <span style="padding: 10px 20px; border-radius: 25px; font-weight: bold; color: white; background: {item.status === 'lost' ? '#ea580c' : '#059669'}; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
              {item.status.toUpperCase()}
            </span>
          </div>
        </div>
        
        <!-- Content Section -->
        <div style="padding: 40px;">
          
          <!-- Title and Description -->
          <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 36px; font-weight: bold; color: #1f2937; margin: 0 0 15px 0;">{item.title}</h1>
            <p style="font-size: 18px; color: #6b7280; line-height: 1.6; margin: 0;">{item.description}</p>
          </div>
          
          <!-- Info Grid -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px;">
            
            <!-- Location -->
            <div style="background: white; padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #f1f5f9;">
              <div style="font-size: 40px; margin-bottom: 15px; color: #2563eb;">📍</div>
              <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 10px 0; color: #1e293b;">Location</h3>
              <p style="font-size: 14px; margin: 0; color: #64748b; font-weight: 500;">{item.location_name.split(' → ').slice(0, 3).join(' → ')}</p>
            </div>
            
            <!-- Reporter -->
            <div style="background: white; padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #f1f5f9;">
              <div style="font-size: 40px; margin-bottom: 15px; color: #7c3aed;">👤</div>
              <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 10px 0; color: #1e293b;">Reporter</h3>
              <p style="font-size: 14px; margin: 0; color: #64748b; font-weight: 500;">{item.reporter_name}</p>
            </div>
            
            <!-- Category -->
            <div style="background: white; padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #f1f5f9;">
              <div style="font-size: 40px; margin-bottom: 15px; color: #059669;">{getCategoryIcon(item.category)}</div>
              <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 10px 0; color: #1e293b;">Category</h3>
              <p style="font-size: 14px; margin: 0; text-transform: capitalize; color: #64748b; font-weight: 500;">{item.category}</p>
            </div>
            
            <!-- Date -->
            <div style="background: white; padding: 25px; border-radius: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #f1f5f9;">
              <div style="font-size: 40px; margin-bottom: 15px; color: {item.status === 'lost' ? '#ea580c' : '#d97706'};">📅</div>
              <h3 style="font-size: 18px; font-weight: 700; margin: 0 0 10px 0; color: #1e293b;">Date</h3>
              <p style="font-size: 14px; margin: 0; color: #64748b; font-weight: 500;">{new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</p>
            </div>
            
          </div>
          
          <!-- Contact Section -->
          <div style="text-align: center;">
            {#if item.status === 'found'}
              <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); border: 1px solid #f1f5f9;">
                <div style="font-size: 80px; margin-bottom: 20px; color: #059669;">🎉</div>
                <h2 style="font-size: 32px; font-weight: bold; margin: 0 0 20px 0; color: #1e293b;">Contact Available!</h2>
                <div style="background: linear-gradient(135deg, #bbf7d0, #86efac); padding: 25px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 25px;">
                  <p style="font-size: 20px; font-weight: bold; margin: 0 0 10px 0; color: #047857;">{item.reporter_name}</p>
                  <p style="font-size: 20px; font-weight: bold; margin: 0; color: #047857;">{item.reporter_phone}</p>
                </div>
                <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                  <a 
                    href="/chat/item_{item.id}"
                    style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; padding: 15px 25px; border-radius: 15px; font-weight: bold; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s;"
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'"
                  >
                    💬 Start Chat
                  </a>
                  <a 
                    href="tel:{item.reporter_phone}"
                    style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 15px 25px; border-radius: 15px; font-weight: bold; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s;"
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'"
                  >
                    📞 Call Now
                  </a>
                </div>
              </div>
            {:else}
              <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); border: 1px solid #f1f5f9;">
                <div style="font-size: 80px; margin-bottom: 20px; color: {item.status === 'lost' ? '#ea580c' : '#d97706'};">🔒</div>
                <h2 style="font-size: 32px; font-weight: bold; margin: 0 0 15px 0; color: #1e293b;">Unlock Contact Info</h2>
                <p style="font-size: 18px; margin: 0 0 10px 0; color: #64748b;">Pay {pricingInfo ? pricingInfo.unlock_price.toLocaleString() : '1,000'} RWF to get reporter's contact details</p>
                {#if pricingInfo}
                  <p style="font-size: 14px; margin: 0 0 30px 0; color: #9ca3af;">Finder gets {pricingInfo.finder_amount.toLocaleString()} RWF • System fee {pricingInfo.system_commission.toLocaleString()} RWF</p>
                {:else}
                  <p style="font-size: 14px; margin: 0 0 30px 0; color: #9ca3af;">Loading pricing...</p>
                {/if}
                <button 
                  on:click={() => showPayment = true}
                  style="background: linear-gradient(135deg, {item.status === 'lost' ? '#ea580c, #c2410c' : '#d97706, #b45309'}); color: white; padding: 15px 40px; border-radius: 15px; font-weight: bold; font-size: 18px; border: none; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all 0.2s ease;"
                  onmouseover="this.style.transform='scale(1.05)'"
                  onmouseout="this.style.transform='scale(1)'"
                >
                  💰 Pay {pricingInfo ? pricingInfo.unlock_price.toLocaleString() : '1,000'} RWF to Unlock
                </button>
              </div>
            {/if}
          </div>
          
        </div>
      </div>
      
      <!-- Payment Modal -->
      {#if showPayment}
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 20px;">
          <div style="background: white; border-radius: 20px; padding: 40px; max-width: 400px; width: 100%;">
            <div style="text-align: center; margin-bottom: 30px;">
              <div style="font-size: 60px; margin-bottom: 15px;">💳</div>
              <h2 style="font-size: 28px; font-weight: bold; color: #1f2937; margin: 0 0 10px 0;">Complete Payment</h2>
              <p style="color: #6b7280; margin: 0;">Pay {pricingInfo ? pricingInfo.unlock_price.toLocaleString() : '1,000'} RWF to unlock contact information</p>
              {#if pricingInfo}
                <p style="color: #9ca3af; margin: 10px 0 0 0; font-size: 14px;">Category: {item.category} • Finder gets {pricingInfo.finder_amount.toLocaleString()} RWF</p>
              {/if}
            </div>
            
            <div style="margin-bottom: 20px;">
              <label style="display: block; font-weight: bold; color: #374151; margin-bottom: 8px;">Payment Method</label>
              <div style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 10px; font-size: 16px; background: #f9fafb; color: #374151; font-weight: 600;">
                📱 MTN Mobile Money Only
              </div>
            </div>
            
            <div style="margin-bottom: 30px;">
              <label style="display: block; font-weight: bold; color: #374151; margin-bottom: 8px;">Phone Number</label>
              <input 
                bind:value={payerPhone} 
                placeholder="0788 123 456" 
                style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 10px; font-size: 16px;"
              />
            </div>
            
            <div style="display: flex; gap: 15px;">
              <button 
                on:click={() => showPayment = false}
                style="flex: 1; background: #f3f4f6; color: #374151; padding: 12px; border-radius: 10px; font-weight: bold; border: none; cursor: pointer;"
              >
                Cancel
              </button>
              <button 
                on:click={processPayment}
                style="flex: 1; background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 12px; border-radius: 10px; font-weight: bold; border: none; cursor: pointer;"
              >
                Pay Now
              </button>
            </div>
          </div>
        </div>
      {/if}
      
    </div>
  {:else}
    <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
      <div style="text-align: center; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <div style="font-size: 80px; margin-bottom: 20px;">😕</div>
        <h1 style="font-size: 32px; font-weight: bold; color: #1f2937; margin: 0 0 15px 0;">Item Not Found</h1>
        <p style="color: #6b7280; margin: 0 0 30px 0; font-size: 16px;">The item you're looking for doesn't exist.</p>
        <a href="/" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; padding: 15px 30px; border-radius: 15px; font-weight: bold; text-decoration: none; display: inline-block;">
          Back to Home
        </a>
      </div>
    </div>
  {/if}
</div>

<style>
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>