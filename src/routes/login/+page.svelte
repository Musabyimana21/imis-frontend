<script>
  import { goto } from '$app/navigation';
  import { login, isAuthenticated } from '$lib/stores/auth';
  import { onMount } from 'svelte';
  import { env } from '$env/dynamic/public';

  let isLogin = true;
  let loading = false;
  let error = '';
  let success = '';

  // Login form
  let loginData = {
    email: '',
    password: ''
  };

  // Register form
  let registerData = {
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    phone: ''
  };

  onMount(() => {
    if ($isAuthenticated) {
      goto('/');
    }
  });

  async function handleLogin() {
    if (!loginData.email || !loginData.password) {
      error = 'Please fill in all fields';
      return;
    }

    loading = true;
    error = '';

    try {
      await login(loginData.email, loginData.password);
      success = 'Login successful! Redirecting...';
      setTimeout(() => goto('/'), 1000);
    } catch (err) {
      error = err.message || 'Login failed. Please check your credentials.';
    } finally {
      loading = false;
    }
  }

  async function handleRegister() {
    if (!registerData.email || !registerData.password || !registerData.full_name) {
      error = 'Please fill in all required fields';
      return;
    }

    if (registerData.password !== registerData.confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    if (registerData.password.length < 6) {
      error = 'Password must be at least 6 characters long';
      return;
    }

    loading = true;
    error = '';

    try {
      const response = await fetch(`${env.PUBLIC_API_URL || 'http://localhost:8000'}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: registerData.email,
          password: registerData.password,
          full_name: registerData.full_name,
          phone: registerData.phone
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      success = 'Registration successful! Please login with your credentials.';
      isLogin = true;
      registerData = { email: '', password: '', confirmPassword: '', full_name: '', phone: '' };
    } catch (err) {
      error = err.message || 'Registration failed. Please try again.';
    } finally {
      loading = false;
    }
  }

  function toggleMode() {
    isLogin = !isLogin;
    error = '';
    success = '';
  }

  function handleQuickLogin(email, password) {
    loginData.email = email;
    loginData.password = password;
    handleLogin();
  }
</script>

<svelte:head>
  <title>{isLogin ? 'Login' : 'Register'} - Ishakiro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4">
  <div class="max-w-4xl w-full">
    <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
      <div class="md:flex">
        <!-- Left Side - Form -->
        <div class="md:w-1/2 p-8 lg:p-12">
          <div class="text-center mb-8">
            <div class="flex items-center justify-center gap-3 mb-6">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl flex items-center justify-center">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              <span class="text-2xl font-bold text-gray-800">Ishakiro</span>
            </div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">
              {isLogin ? 'Welcome Back' : 'Create Account'}
            </h1>
            <p class="text-gray-600">
              {isLogin ? 'Sign in to your account to continue' : 'Join Rwanda\'s lost and found community'}
            </p>
          </div>

          <!-- Alert Messages -->
          {#if error}
            <div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-center gap-3">
                <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="text-red-700 text-sm">{error}</span>
              </div>
            </div>
          {/if}

          {#if success}
            <div class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div class="flex items-center gap-3">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span class="text-green-700 text-sm">{success}</span>
              </div>
            </div>
          {/if}

          <!-- Login Form -->
          {#if isLogin}
            <form on:submit|preventDefault={handleLogin} class="space-y-6">
              <div class="form-group">
                <label for="email" class="form-label">Email Address</label>
                <input
                  type="email"
                  id="email"
                  bind:value={loginData.email}
                  class="form-control"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div class="form-group">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  id="password"
                  bind:value={loginData.password}
                  class="form-control"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                class="w-full btn btn-primary btn-large {loading ? 'opacity-50 cursor-not-allowed' : ''}"
              >
                {#if loading}
                  <div class="loading">
                    <div class="spinner"></div>
                    Signing In...
                  </div>
                {:else}
                  Sign In
                {/if}
              </button>
            </form>
          {:else}
            <!-- Register Form -->
            <form on:submit|preventDefault={handleRegister} class="space-y-6">
              <div class="form-group">
                <label for="full_name" class="form-label">Full Name</label>
                <input
                  type="text"
                  id="full_name"
                  bind:value={registerData.full_name}
                  class="form-control"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div class="form-group">
                <label for="reg_email" class="form-label">Email Address</label>
                <input
                  type="email"
                  id="reg_email"
                  bind:value={registerData.email}
                  class="form-control"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div class="form-group">
                <label for="phone" class="form-label">Phone Number (Optional)</label>
                <input
                  type="tel"
                  id="phone"
                  bind:value={registerData.phone}
                  class="form-control"
                  placeholder="+250 788 000 000"
                />
              </div>

              <div class="form-group">
                <label for="reg_password" class="form-label">Password</label>
                <input
                  type="password"
                  id="reg_password"
                  bind:value={registerData.password}
                  class="form-control"
                  placeholder="Create a password (min. 6 characters)"
                  required
                />
              </div>

              <div class="form-group">
                <label for="confirm_password" class="form-label">Confirm Password</label>
                <input
                  type="password"
                  id="confirm_password"
                  bind:value={registerData.confirmPassword}
                  class="form-control"
                  placeholder="Confirm your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                class="w-full btn btn-primary btn-large {loading ? 'opacity-50 cursor-not-allowed' : ''}"
              >
                {#if loading}
                  <div class="loading">
                    <div class="spinner"></div>
                    Creating Account...
                  </div>
                {:else}
                  Create Account
                {/if}
              </button>
            </form>
          {/if}

          <!-- Toggle Mode -->
          <div class="mt-8 text-center">
            <p class="text-gray-600">
              {isLogin ? "Don't have an account?" : 'Already have an account?'}
              <button
                on:click={toggleMode}
                class="text-blue-600 hover:text-blue-700 font-semibold ml-1"
              >
                {isLogin ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>

          <!-- Quick Login (Development) -->
          {#if isLogin}
            <div class="mt-8 p-4 bg-gray-50 rounded-lg">
              <h3 class="text-sm font-semibold text-gray-700 mb-3">Quick Login (Demo)</h3>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <button
                  on:click={() => handleQuickLogin('admin@imis.rw', 'admin123')}
                  class="p-2 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
                >
                  Admin
                </button>
                <button
                  on:click={() => handleQuickLogin('loser@imis.rw', 'lost123')}
                  class="p-2 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
                >
                  Loser
                </button>
                <button
                  on:click={() => handleQuickLogin('finder@imis.rw', 'found123')}
                  class="p-2 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                >
                  Finder
                </button>
                <button
                  on:click={() => handleQuickLogin('user1@imis.rw', 'password123')}
                  class="p-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
                >
                  User
                </button>
              </div>
            </div>
          {/if}
        </div>

        <!-- Right Side - Info -->
        <div class="md:w-1/2 bg-gradient-to-br from-blue-600 to-blue-800 p-8 lg:p-12 text-white">
          <div class="h-full flex flex-col justify-center">
            <h2 class="text-3xl font-bold mb-6">
              {isLogin ? 'Welcome to Ishakiro' : 'Join Our Community'}
            </h2>
            
            <div class="space-y-6">
              <div class="flex items-start gap-4">
                <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold mb-2">Lightning Fast</h3>
                  <p class="text-blue-100 text-sm">Report lost or found items in under 30 seconds with our streamlined process.</p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold mb-2">AI-Powered Matching</h3>
                  <p class="text-blue-100 text-sm">Advanced algorithms with 89% accuracy to connect you with the right matches.</p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold mb-2">Secure & Safe</h3>
                  <p class="text-blue-100 text-sm">Protected messaging and verified users ensure safe interactions throughout Rwanda.</p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold mb-2">Mobile Money Integration</h3>
                  <p class="text-blue-100 text-sm">Pay 1,000 RWF via MTN MoMo or Airtel Money to unlock contact information.</p>
                </div>
              </div>
            </div>

            <div class="mt-8 p-4 bg-white/10 rounded-lg">
              <div class="flex items-center gap-3 mb-2">
                <span class="text-2xl">🇷🇼</span>
                <span class="font-semibold">Made for Rwanda</span>
              </div>
              <p class="text-blue-100 text-sm">
                Designed specifically for Rwandans, with local payment methods and bilingual support.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>