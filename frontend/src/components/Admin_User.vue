<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3 d-flex align-items-center">
          <i class="fas fa-user-shield me-2"></i>Admin Dashboard
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin">
                <i class="fas fa-home me-1"></i>Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_summary">
                <i class="fas fa-chart-line me-1"></i>Summary
              </router-link>
            </li>
          </ul>
          <form class="d-flex me-3">
            <div class="input-group">
              <input class="form-control form-control-sm" type="search" placeholder="Search users..." v-model="searchQuery" aria-label="Search" />
              <button class="btn btn-light btn-sm" type="button">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </form>
          <router-link to="/login" class="btn btn-outline-light btn-sm">
            <i class="fas fa-sign-out-alt me-1"></i>Logout
          </router-link>
        </div>
      </div>
    </nav>

    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-9">
          <div class="card shadow-lg border-0 rounded-3">
            <div class="card-header bg-primary text-white text-center py-3 rounded-top-3">
              <h4 class="mb-0">
                <i class="fas fa-users me-2"></i>User Details
              </h4>
            </div>

            <div v-if="filteredUsers.length === 0" class="card-body text-center p-4">
              <p class="lead text-muted">
                <i class="fas fa-exclamation-circle me-1"></i>No users found.
              </p>
            </div>
            <div v-else>
              <div v-for="user in filteredUsers" :key="user.id" class="card-body border-bottom p-4">
                <div class="d-flex align-items-start mb-3">
                  <i class="fas fa-id-card fa-2x text-primary me-3"></i>
                  <div>
                    <h5 class="card-title mb-1">{{ user.full_name }}</h5>
                    <span class="badge bg-secondary text-white">{{ user.username }}</span>
                  </div>
                </div>
                <ul class="list-group list-group-flush mb-3">
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong><i class="fas fa-envelope me-2 text-muted"></i>Email:</strong>
                    <span>{{ user.email }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong><i class="fas fa-birthday-cake me-2 text-muted"></i>Date of Birth:</strong>
                    <span>{{ user.dob }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong><i class="fas fa-venus-mars me-2 text-muted"></i>Gender:</strong>
                    <span>{{ user.gender }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong><i class="fas fa-phone me-2 text-muted"></i>Phone:</strong>
                    <span>{{ user.phone }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong><i class="fas fa-map-marker-alt me-2 text-muted"></i>Address:</strong>
                    <span>{{ user.address }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <strong><i class="fas fa-user-graduate me-2 text-muted"></i>Qualification:</strong>
                    <span>{{ user.qualification || 'N/A' }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      searchQuery: ''
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user =>
        user.full_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        user.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        user.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin_users`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: 'Bearer ' + localStorage.getItem('admin_token'),
          },
        });
        const data = await response.json();
        this.users = data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>