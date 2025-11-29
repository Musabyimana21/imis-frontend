<script>
  export let item;
  
  const categoryIcons = {
    phone: '📱',
    wallet: '💼',
    keys: '🔑',
    bag: '🎒',
    documents: '📄',
    electronics: '💻',
    jewelry: '💍',
    other: '📦'
  };
  
  const statusConfig = {
    lost: { color: 'from-red-500 to-red-700', bg: 'bg-red-50', border: 'border-red-200' },
    found: { color: 'from-green-500 to-green-700', bg: 'bg-green-50', border: 'border-green-200' },
    matched: { color: 'from-yellow-500 to-yellow-700', bg: 'bg-yellow-50', border: 'border-yellow-200' },
    recovered: { color: 'from-blue-500 to-blue-700', bg: 'bg-blue-50', border: 'border-blue-200' }
  };
  
  function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  }
  
  $: config = statusConfig[item.status] || statusConfig.lost;
</script>

<a href={`/items/${item.id}`} class="block group">
  <div class="card h-full relative">
    <!-- Status Badge -->
    <div class="absolute top-4 right-4 z-10">
      <span class="status-badge {item.status === 'lost' ? 'status-lost' : 'status-found'}">
        {item.status}
      </span>
    </div>
    
    <!-- Content -->
    <div class="space-y-3 pt-8">
      <h3 class="font-bold text-lg" style="color: var(--text) !important;">
        {item.title}
      </h3>
      
      <p class="text-sm line-clamp-2" style="color: var(--text-light) !important;">
        {item.description}
      </p>
      
      <!-- Meta Info -->
      <div class="space-y-2 text-xs pt-2">
        <div style="color: var(--text-muted) !important;">
          📍 {item.location_name}
        </div>
        <div style="color: var(--text-muted) !important;">
          🕒 {formatDate(item.created_at)}
        </div>
      </div>
      
      <!-- ID Badge -->
      <div class="flex justify-between items-center pt-3 border-t border-gray-200">
        <span class="text-xs font-mono" style="color: var(--text-muted) !important;">ID: #{item.id}</span>
        <span class="font-bold" style="color: var(--primary) !important;">
          View Details →
        </span>
      </div>
    </div>
  </div>
</a>
