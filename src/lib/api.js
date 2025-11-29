import { get } from 'svelte/store';
import { token } from './stores/auth';
import { PUBLIC_API_URL } from '$env/static/public';

const API_URL = PUBLIC_API_URL || 'http://localhost:8002';

async function request(endpoint, options = {}) {
  const authToken = get(token);
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }
  
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers
    });
    
    if (!response.ok) {
      let errorMessage = 'Something went wrong';
      
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch (e) {
        if (response.status === 401) {
          errorMessage = 'Invalid credentials. Please check your email and password.';
        } else if (response.status === 400) {
          errorMessage = 'Invalid request. Please check your input.';
        } else if (response.status === 404) {
          errorMessage = 'Resource not found.';
        } else if (response.status === 500) {
          errorMessage = 'Server error. Please try again later.';
        } else {
          errorMessage = `Error: ${response.statusText}`;
        }
      }
      
      throw new Error(errorMessage);
    }
    
    return response.json();
  } catch (error) {
    if (error.message.includes('fetch')) {
      throw new Error('Cannot connect to server. Please make sure the backend is running on http://localhost:8001');
    }
    throw error;
  }
}

export const api = {
  auth: {
    register: (data) => request('/api/auth/register', { method: 'POST', body: JSON.stringify(data) }),
    login: (data) => request('/api/auth/login', { method: 'POST', body: JSON.stringify(data) })
  },
  items: {
    create: (data) => request('/api/items/', { method: 'POST', body: JSON.stringify(data) }),
    getAll: () => request('/api/items/'),
    getOne: (id) => request(`/api/items/${id}`),
    getMatches: (id) => request(`/api/items/${id}/matches`),
    delete: (id) => request(`/api/items/${id}`, { method: 'DELETE' })
  },
  messages: {
    send: (data) => request('/api/messages/', { method: 'POST', body: JSON.stringify(data) }),
    getAll: () => request('/api/messages/'),
    markRead: (id) => request(`/api/messages/${id}/read`, { method: 'PUT' })
  },
  admin: {
    getStats: () => request('/api/admin/stats'),
    getCommissions: () => request('/api/admin/commissions'),
    createCommission: (itemId, amount) => request(`/api/admin/commissions/${itemId}`, { 
      method: 'POST', 
      body: JSON.stringify({ amount }) 
    }),
    getUsers: () => request('/api/admin/users')
  },
  anonymous: {
    report: (data) => request('/api/anonymous/report', { method: 'POST', body: JSON.stringify(data) }),
    getItems: () => request('/api/anonymous/items'),
    track: (code) => request(`/api/anonymous/track/${code}`)
  }
};
