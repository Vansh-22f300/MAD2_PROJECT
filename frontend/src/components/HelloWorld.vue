<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3">
      <div class="container">
        <a class="navbar-brand text-primary fw-bold fs-3" href="#">QuizMaster</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link active fw-semibold" href="#">Home</a></li>
            <li class="nav-item"><a class="nav-link fw-semibold" href="#">Features</a></li>
            <li class="nav-item"><router-link class="nav-link fw-semibold" to="/login">Login</router-link></li>
            <li class="nav-item"><router-link class="btn btn-primary ms-2 fw-semibold" to="/signup">Sign Up</router-link></li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section d-flex align-items-center text-white text-center">
      <div class="container">
        <h1 class="display-3 fw-bold">Ace Your Quizzes with Confidence!</h1>
        <p class="lead">Practice, progress and perform better — all in one place.</p>
        <router-link to="/login" class="btn btn-warning btn-lg px-4 me-2 mt-3 fw-semibold">Start Now</router-link>
        <router-link to="/signup" class="btn btn-outline-light btn-lg px-4 mt-3 fw-semibold">Join Free</router-link>
      </div>
    </header>

    <!-- Features Section -->
    <section class="container py-5">
      <div class="text-center mb-5">
        <h2 class="fw-bold">Features That Set Us Apart</h2>
        <p class="text-muted">Everything you need to grow smarter.</p>
      </div>
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow feature-card text-center p-4">
            <i class="bi bi-lightbulb-fill text-warning fs-1 mb-3"></i>
            <h5 class="fw-bold">Smart Questions</h5>
            <p class="text-muted">Dynamic quizzes tailored to your level, curated by subject experts.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow feature-card text-center p-4">
            <i class="bi bi-graph-up-arrow text-success fs-1 mb-3"></i>
            <h5 class="fw-bold">Track Progress</h5>
            <p class="text-muted">Analyze your results and see improvements over time with detailed reports.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow feature-card text-center p-4">
            <i class="bi bi-trophy-fill text-danger fs-1 mb-3"></i>
            <h5 class="fw-bold">Rewards & Ranks</h5>
            <p class="text-muted">Earn badges and climb leaderboards as you complete milestones.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="cta-section text-white text-center py-5">
      <div class="container">
        <h2 class="fw-bold mb-3">Join 50,000+ learners mastering their skills</h2>
        <p class="lead mb-4">Start your learning journey with QuizMaster today!</p>
        <router-link to="/signup" class="btn btn-light btn-lg px-4 fw-semibold">Create Free Account</router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3">
      <div class="container">
        <small>&copy; 2025 QuizMaster. All rights reserved.</small>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(
      rgba(0, 0, 0, 0.5), 
      rgba(0, 0, 0, 0.5)
    ),
    url('https://images.unsplash.com/photo-1584697964403-b58bbaef5c15?auto=format&fit=crop&w=1500&q=80') no-repeat center center;
  background-size: cover;
  height: 90vh;
}

.feature-card {
  transition: transform 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-10px);
}

.cta-section {
  background: linear-gradient(to right, #0061ff, #60efff);
}
</style>
