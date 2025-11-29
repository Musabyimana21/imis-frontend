import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';

const storedToken = browser ? localStorage.getItem('token') : null;
const storedUser = browser ? JSON.parse(localStorage.getItem('user') || 'null') : null;

export const token = writable(storedToken);
export const user = writable(storedUser);
export const isAuthenticated = writable(!!storedToken);

token.subscribe(value => {
  if (browser) {
    if (value) {
      localStorage.setItem('token', value);
    } else {
      localStorage.removeItem('token');
    }
  }
});

user.subscribe(value => {
  if (browser) {
    if (value) {
      localStorage.setItem('user', JSON.stringify(value));
    } else {
      localStorage.removeItem('user');
    }
  }
});

export async function login(email, password) {
  const API_URL = env.PUBLIC_API_URL || 'http://localhost:8000';
  
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: email,
      password: password
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Login failed');
  }

  const data = await response.json();
  
  token.set(data.access_token);
  user.set(data.user || { email });
  isAuthenticated.set(true);
  
  return data;
}

export function logout() {
  token.set(null);
  user.set(null);
  isAuthenticated.set(false);
}
