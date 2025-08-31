<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">User Dashboard</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/user" class="nav-link active"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/user_results" class="nav-link"><i class="fas fa-chart-bar me-2"></i>My Results</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <div>
          <h2 class="fw-bold">Welcome, {{ username }}!</h2>
          <p class="text-muted">Select a quiz to begin.</p>
        </div>
        <div class="search-wrapper">
          <i class="fas fa-search search-icon"></i>
          <input v-model="searchQuery" class="form-control" type="search" placeholder="Search for a quiz...">
        </div>
      </header>

      <section class="mt-4">
        <div v-if="filteredQuizzes.length === 0" class="alert alert-info text-center">
          <i class="fas fa-exclamation-circle me-2"></i>No quizzes found.
        </div>
        
        <div class="row g-4" v-else>
          <div class="col-md-6 col-lg-4" v-for="quiz in filteredQuizzes" :key="quiz.id">
            <div class="quiz-card-v2 h-100">
              <div class="quiz-card-v2-header">
                <span class="quiz-subject-badge">{{ quiz.subject_name }}</span>
                <h5 class="fw-bold mt-2 mb-1">{{ quiz.title }}</h5>
                <p class="text-muted small mb-0">{{ quiz.chapter_name }}</p>
              </div>
              <div class="quiz-card-v2-body">
                <div v-if="quiz.score !== null && quiz.score !== undefined" class="mb-3">
                  <span class="badge status-badge active">
                    <i class="fas fa-trophy me-1"></i>Score: {{ quiz.score }}/{{ quiz.total }}
                  </span>
                </div>
                
                <ul class="quiz-details-list-user">
                  <li><i class="fas fa-clock"></i><span>{{ quiz.time_limit }} Minutes</span></li>
                  <li><i :class="quiz.single_attempt ? 'fas fa-check-circle' : 'fas fa-redo'"></i><span>{{ quiz.single_attempt ? 'Single Attempt' : 'Multiple Attempts' }}</span></li>
                </ul>
              </div>
              <div class="quiz-card-v2-footer">
                <router-link :to="'/start_quiz/' + quiz.id" class="btn btn-primary-custom w-100">
                  <i class="fas fa-play-circle me-2"></i>
                  {{ (quiz.score !== null && quiz.score !== undefined) ? 'Attempt Again' : 'Start Quiz' }}
                </router-link>
              </div>
            </div>
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
      username: '',
      searchQuery: '',
      quizzes: [],
    };
  },
  computed: {
    filteredQuizzes() {
    // 1. If the search bar is empty, show all quizzes
    if (!this.searchQuery) {
      return this.quizzes;
    }
    
    // 2. Prepare the search query (lowercase and no extra spaces)
    const query = this.searchQuery.toLowerCase().trim();
    
    return this.quizzes.filter(quiz => {
      // 3. Safely check for a match in the title, subject, OR chapter
      const titleMatch = quiz.title && quiz.title.toLowerCase().includes(query);
      const subjectMatch = quiz.subject_name && quiz.subject_name.toLowerCase().includes(query);
      const chapterMatch = quiz.chapter_name && quiz.chapter_name.toLowerCase().includes(query);
      
      return titleMatch || subjectMatch || chapterMatch;
    });
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

