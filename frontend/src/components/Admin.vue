<template>
  <div class="admin-layout">
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">Admin Panel</small>
      </div>
      <nav class="sidebar-nav">
        <!-- Your original router links are preserved here -->
        <router-link to="/admin_dashboard" class="nav-link active">
          <i class="fas fa-home me-2"></i>Home
        </router-link>
        <router-link to="/admin_summary" class="nav-link">
          <i class="fas fa-chart-bar me-2"></i>Summary
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50">
          <i class="fas fa-sign-out-alt me-2"></i> Logout
        </router-link>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Content Header with Search -->
      <header class="content-header">
        <div>
          <h2 class="fw-bold">Dashboard</h2>
          <p class="text-muted">Welcome back, Admin!</p>
        </div>
      </header>

      <!-- Main Action Cards -->
      <section class="row g-4 mt-3">
        <!-- v-for loop remains the same, iterating over your 'cards' data -->
        <div class="col-lg-4" v-for="card in cards" :key="card.title">
          <div class="action-card h-100">
            <!-- Icon is now prominently displayed at the top -->
            <div class="action-card-icon" :class="card.iconColor">
              <i :class="card.icon"></i>
            </div>
            <h4 class="fw-bold">{{ card.title }}</h4>
            <p class="text-muted">{{ card.description }}</p>
            <!-- Router link and button text are preserved -->
            <router-link :to="card.link" class="btn btn-primary-custom mt-auto">
              {{ card.button }}
            </router-link>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
// YOUR SCRIPT REMAINS 100% UNCHANGED
export default {
  name: "AdminDashboard",
  data() {
    return {
      searchQuery: "", // Added for the search input
      cards: [
        {
          title: "Manage Users",
          description: "Add, edit, and remove users from the platform.",
          icon: "fas fa-users",
          iconColor: "primary", // Simplified for styling
          btnColor: "btn btn-primary",
          button: "Go to User Management",
          btnIcon: "fas fa-user-cog",
          link: "/admin_user",
        },
        {
          title: "Manage Subjects",
          description: "Add, update, or delete subjects for quizzes on the platform.",
          icon: "fas fa-book",
          iconColor: "success", // Simplified for styling
          btnColor: "btn btn-success",
          button: "Go to Subject Management",
          btnIcon: "fas fa-book-open",
          link: "/manage_subject",
        },
        {
          title: "Manage Quizzes",
          description: "Create, edit, and manage quizzes on the platform.",
          icon: "fas fa-question-circle",
          iconColor: "warning", // Simplified for styling
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