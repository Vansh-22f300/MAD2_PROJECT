<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3">
          <i class="fas fa-user-circle me-2"></i>Welcome, Admin
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin_dashboard">
                <i class="fas fa-home me-1"></i>Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_summary">
                <i class="fas fa-chart-bar me-1"></i>Summary
              </router-link>
            </li>
          </ul>
          <form class="d-flex me-3">
            <div class="input-group">
              <input class="form-control" type="search" placeholder="Search..." v-model="searchQuery" />
              <button class="btn btn-light" type="button">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </form>
          <router-link to="/login" class="btn btn-outline-light">
            <i class="fas fa-sign-out-alt me-1"></i>Logout
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-4 mb-4" v-for="card in cards" :key="card.title">
          <div class="card h-100 text-center shadow">
            <div class="card-body">
              <h5 class="card-title">{{ card.title }}</h5>
              <p class="card-text">{{ card.description }}</p>
              <router-link :to="card.link" class="btn btn-lg mt-3" :class="card.btnColor">
                <i :class="card.btnIcon + ' me-2'"></i>{{ card.button }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      cards: [
        {
          title: "Manage Users",
          description: "Add, edit, and remove users from the platform.",
          icon: "fas fa-users",
          iconColor: "text-primary",
          btnColor: "btn btn-primary",
          button: "Go to User Management",
          btnIcon: "fas fa-user-cog",
          link: "/admin_user",
        },
        {
          title: "Manage Subjects",
          description: "Add, update, or delete subjects for quizzes on the platform.",
          icon: "fas fa-book",
          iconColor: "text-success",
          btnColor: "btn btn-success",
          button: "Go to Subject Management",
          btnIcon: "fas fa-book-open",
          link: "/manage_subject",
        },
        {
          title: "Manage Quizzes",
          description: "Create, edit, and manage quizzes on the platform.",
          icon: "fas fa-question-circle",
          iconColor: "text-warning",
          btnColor: "btn btn-warning",
          button: "Go to Quiz Management",
          btnIcon: "fas fa-edit",
          link: "/manage_quiz",
        },
      ],
    };
  },
};
</script>

<style scoped>
body {
  font-family: 'Segoe UI', sans-serif;
}
</style>
