<template>
  <div class="auth-container d-flex align-items-center justify-content-center">
    <div class="auth-card shadow-lg p-4 p-sm-5">
      <div class="text-center mb-4">
        <i class="bi bi-shield-lock-fill brand-icon"></i>
        <h3 class="mt-3 fw-bold">Welcome Back</h3>
        <p class="text-muted small">Login to continue your quiz journey</p>
      </div>
      
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-control"
            id="username"
            placeholder="Enter your username"
            required
          />
        </div>
        
        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
            placeholder="Enter your password"
            required
          />
        </div>
        
        <button type="submit" class="btn btn-primary-custom w-100 fw-semibold mt-2">Login</button>
      </form>
      
      <div class="text-center mt-4">
        <small class="text-muted">Don't have an account? <router-link to="/signup">Sign Up</router-link></small>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      const response = await fetch('https://quiz-app-v2-py9b.onrender.com/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: this.username, password: this.password })
      });

      const data = await response.json();
          if (response.ok) {
        if (data.username === 'admin') {
          localStorage.setItem('admin_username', data.username);
          localStorage.setItem('admin_id', data.user_id);
          localStorage.setItem('admin_token', data.access_token); // ✅ fixed
          this.$router.push('/admin');
        } else {
          localStorage.setItem('user_username', data.username);
          localStorage.setItem('user_id', data.user_id);
          localStorage.setItem('user_token', data.access_token); // ✅ fixed
          this.$router.push('/user');
        }
      } else {
        alert(data.message);
      }
    }
  }
};
</script>

