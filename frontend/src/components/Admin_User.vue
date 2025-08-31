<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">Admin Panel</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-link"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/admin_summary" class="nav-link"><i class="fas fa-chart-bar me-2"></i>Summary</router-link>
        <router-link to="/manage_quiz" class="nav-link"><i class="fas fa-clipboard-list me-2"></i>Manage Quizzes</router-link>
        <router-link to="/admin_user" class="nav-link active"><i class="fas fa-users-cog me-2"></i>Manage Users</router-link>
        <router-link to="/manage_subject" class="nav-link"><i class="fas fa-book me-2"></i>Manage Subjects</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <div>
          <h2 class="fw-bold">User Management</h2>
          <p class="text-muted">View and search for registered users.</p>
        </div>
        <div class="search-wrapper">
          <i class="fas fa-search search-icon"></i>
          <input class="form-control" type="search" placeholder="Search users..." v-model="searchQuery" />
        </div>
      </header>

      <section class="mt-4">
        <div class="data-card">
          <div v-if="filteredUsers.length === 0" class="text-center p-5">
            <i class="fas fa-exclamation-circle fa-2x text-muted mb-3"></i>
            <p class="lead text-muted">No users found matching your search.</p>
          </div>

          <div class="table-responsive" v-else>
            <table class="table modern-table">
              <thead>
                <tr>
                  <th>Full Name</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Gender</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>
                    <div class="fw-bold">{{ user.full_name }}</div>
                  </td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.phone }}</td>
                  <td>
                    <span class="badge status-badge" :class="user.gender === 'Male' ? 'male' : (user.gender === 'Female' ? 'female' : 'other')">
                      {{ user.gender }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
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
        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/admin_users`, {
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