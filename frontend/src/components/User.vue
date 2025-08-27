<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-4 py-2">
      <span class="navbar-text text-white me-3">
        <i class="fas fa-user-circle me-2"></i> Welcome, <strong>{{ username }}</strong>
      </span>
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><router-link class="nav-link text-white" to="/user"><i class="fas fa-home me-1"></i>Home</router-link></li>
        <li class="nav-item"><router-link class="nav-link text-white" to="/user_results"><i class="fas fa-chart-bar me-1"></i>User Results</router-link></li>
      </ul>
      <form class="d-flex me-3">
        <div class="input-group">
          <input v-model="searchQuery" class="form-control" type="search" placeholder="Search quiz...">
          <button class="btn btn-light" type="button" @click="searchQuiz"><i class="fas fa-search"></i></button>
        </div>
      </form>
      <router-link to="/login" class="btn btn-outline-light">
        <i class="fas fa-sign-out-alt me-1"></i>Logout
      </router-link>
    </nav>

    <!-- Welcome Banner -->
    <div class="text-white text-center py-5" style="background-color: #6827b7; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;">
      <h2><i class="fas fa-mortar-board me-2"></i> Welcome, <span class="fw-bold text-warning">{{ username }}!</span></h2>
      <p class="mb-0">Your personalized quiz dashboard to track your progress and take new challenges.</p>
    </div>

    <!-- Quiz Section -->
    <div class="container my-5">
      <h3 class="text-center text-primary fw-bold mb-4">
        <i class="fas fa-clipboard-list me-2"></i> Available Quizzes
      </h3>

      <div class="p-4 rounded shadow bg-white">
        <div class="row g-4">
          <div class="col-md-4" v-for="quiz in filteredQuizzes" :key="quiz.id">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title text-primary"><i class="fas fa-book me-2"></i>{{ quiz.title }}</h5>
                <p><i class="fas fa-book-open me-2"></i>Subject: {{ quiz.subject_name }}</p>
                <p><i class="fas fa-bookmark me-2"></i>Chapter: {{ quiz.chapter_name }}</p>
                <p><i class="fas fa-info-circle me-2"></i>{{ quiz.description || 'Quiz Description' }}</p>
                <p>
                  <i :class="quiz.single_attempt ? 'fas fa-check-circle text-success' : 'fas fa-redo text-warning'" class="me-2"></i>
                  {{ quiz.single_attempt ? 'Single Attempt' : 'Multiple Attempts' }}
                </p>
                <p><i class="fas fa-calendar-alt me-2"></i>{{ quiz.date }} | <i class="fas fa-clock me-2"></i>{{ quiz.time_limit }} Minutes</p>
                <div v-if="quiz.score !== null && quiz.score !== undefined" class="alert alert-success py-2 mt-2 mb-2">
                  <i class="fas fa-trophy me-2"></i>Your Score: {{ quiz.score }}/{{ quiz.total }}
                </div>
                <div class="d-grid gap-2">
                  <router-link :to="'/start_quiz/' + quiz.id" class="btn btn-primary">
                    <i class="fas fa-play-circle me-2"></i>Start Quiz
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredQuizzes.length === 0" class="alert alert-warning text-center mt-4">
          <i class="fas fa-exclamation-circle me-2"></i>No quizzes found for "{{ searchQuery }}"
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      username: '',
      searchQuery: '',
      quizzes: [],
    };
  },
  computed: {
    filteredQuizzes() {
      const q = this.searchQuery.toLowerCase();
      return this.quizzes.filter(quiz => quiz.title.toLowerCase().includes(q));
    }
  },
  methods: {
    fetchQuizzes() {
      fetch('https://quiz-app-v2-py9b.onrender.com/get_quiz', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('user_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        console.log('Fetched quizzes:', data);

        this.quizzes = data.map(quiz => ({
          ...quiz,
          Is_active: typeof quiz.Is_active === 'string' ? (quiz.Is_active === 'true') : !!quiz.Is_active,
          single_attempt: !!quiz.single_attempt
        }));
      })
      .catch(error => {
        console.error('Error fetching quizzes:', error);
      });
    },
    searchQuiz() {},
    startQuiz(id) {
      this.$router.push(`/start_quiz/${id}`);
    },
    logout() {
      localStorage.removeItem('user_token');
      this.$router.push('/login');
    },
    async getUsername() {
    try {
      const res = await fetch('https://quiz-app-v2-py9b.onrender.com/user/profile', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('user_token')
        }
      });
      const data = await res.json();
      if (res.ok) {
        this.username = data.username;
      } else {
        console.error(data.message);
      }
    } catch (err) {
      console.error('Error:', err);
    }
  }
  },
  mounted() {
    this.fetchQuizzes();
    
    this.getUsername();

  },
};
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
  background-color: #f0f2f5;
  min-height: 100vh;
}
</style>
