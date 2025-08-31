<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">User Dashboard</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/user" class="nav-link"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/user_results" class="nav-link active"><i class="fas fa-chart-bar me-2"></i>My Results</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <div>
          <h2 class="fw-bold">My Score Report</h2>
          <p class="text-muted">A summary of all your quiz attempts.</p>
        </div>
        <div class="d-flex align-items-center gap-3">
            <div class="search-wrapper">
              <i class="fas fa-search search-icon"></i>
              <input class="form-control" type="search" placeholder="Search results..." v-model="searchQuery" />
            </div>
            <button class="btn btn-primary-custom" @click="exportCSV">
              <i class="fas fa-file-csv me-2"></i>Export CSV
            </button>
        </div>
      </header>

      <section class="mt-4">
        <div class="data-card">
          <div v-if="filteredScores.length === 0" class="text-center p-5">
            <i class="fas fa-box-open fa-2x text-muted mb-3"></i>
            <p class="lead text-muted">You haven't completed any quizzes yet.</p>
          </div>

          <div class="table-responsive" v-else>
            <table class="table modern-table">
              <thead>
                <tr>
                  <th>Quiz Title</th>
                  <th>Score</th>
                  <th>Percentage</th>
                  <th>Grade</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in filteredScores" :key="score.id">
                  <td>
                    <div class="fw-bold">{{ score.quiz_title }}</div>
                    <small class="text-muted">{{ score.subject_name }} / {{ score.chapter_name }}</small>
                  </td>
                  <td>
                    <span class="fw-bold">{{ score.score }} / {{ score.total_possible_marks }}</span>
                  </td>
                  <td>
                    <div class="progress-wrapper">
                      <div class="progress" style="height: 20px;">
                        <div class="progress-bar" role="progressbar" :style="{ width: score.percentage + '%' }" :aria-valuenow="score.percentage" aria-valuemin="0" aria-valuemax="100">
                          {{ score.percentage }}%
                        </div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="badge status-badge" :class="getGradeClass(score.grade)">{{ score.grade }}</span>
                  </td>
                  <td>{{ formatDateTime(score.date_taken) }}</td>
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
      scores: [],
      searchQuery: '',
      username: ''
    };
  },
  computed: {
    filteredScores() {
      const query = this.searchQuery.toLowerCase();
      return this.scores.filter(score =>
        score.quiz_title.toLowerCase().includes(query) ||
        score.subject_name.toLowerCase().includes(query) ||
        score.chapter_name.toLowerCase().includes(query)
      );
    }
  },
  methods: {
    fetchScores() {
      fetch('https://quiz-app-v2-py9b.onrender.com/user_results', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('user_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        this.scores = data;
      })
      .catch(error => {
        console.error('Error fetching scores:', error);
      });
    },
    getGradeClass(grade) {
      if (grade === 'Excellent') return 'active'; // Uses the green 'active' style
      if (grade === 'Good') return 'male'; // Re-using the blue style
      return 'inactive'; 
    },
    formatDateTime(utcDateString) {
    if (!utcDateString) return 'N/A';
    
    const date = new Date(utcDateString + 'Z'); 
    
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
      // timeZoneName: 'short' // Optional: adds timezone like "IST"
    };
    
    // This will now use the user's local timezone for formatting
    return new Intl.DateTimeFormat('en-IN', options).format(date);
  },
    fetchUsername() {
      fetch('https://quiz-app-v2-py9b.onrender.com/user/profile', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('user_token')
        }
      })
      .then(res => res.json())
      .then(data => {
        this.username = data.username;
      })
      .catch(err => {
        console.error('Error fetching username:', err);
      });
    },
    exportCSV() {
      fetch('https://quiz-app-v2-py9b.onrender.com/export_details', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('user_token')
        }
      })
      .then(response => {
        if (response.ok) return response.blob();{
        throw new Error("Failed to export.");
        }
        return response.blob();
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'user_scores.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error exporting CSV:', error);
      });
    },
    searchQuiz() {
      console.log("Searching for:", this.searchQuery);
    }
  },
  mounted() {
    this.fetchScores();
    this.fetchUsername();
  }
};
</script>
