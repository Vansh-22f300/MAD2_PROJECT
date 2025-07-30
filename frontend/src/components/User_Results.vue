<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-4 py-2 mb-4">
      <span class="navbar-text text-white me-3">
        <i class="fas fa-user-circle me-2"></i> Welcome, <strong>{{ username }}</strong>
      </span>
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <router-link class="nav-link text-white" to="/user">
            <i class="fas fa-home me-1"></i>Home
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link text-white" to="/user_results">
            <i class="fas fa-chart-bar me-1"></i>User Results
          </router-link>
        </li>
      </ul>
      <form class="d-flex me-3">
        <div class="input-group">
          <input v-model="searchQuery" class="form-control" type="search" placeholder="Search quiz/subject/chapter">
          <button class="btn btn-light" type="button" @click="searchQuiz">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </form>
      <router-link to="/login" class="btn btn-outline-light">
        <i class="fas fa-sign-out-alt me-1"></i>Logout
      </router-link>
    </nav>

    <!-- Scores Table -->
    <div class="container">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h3 class="text-center mb-4 text-primary">
            <i class="fas fa-star me-2"></i>User Score Report
          </h3>

          <div class="table-responsive">
            <table class="table table-bordered table-hover align-middle">
              <thead class="table-primary text-center">
                <tr>
                  <th>Subject</th>
                  <th>Chapter</th>
                  <th>Quiz</th>
                  <th>Score</th>
                  <th>Total Marks</th>
                  <th>Percentage</th>
                  <th>Grade</th>
                  <th>Date & Time</th>
                </tr>
              </thead>
              <tbody class="text-center">
                <tr v-for="score in filteredScores" :key="score.id">
                  <td>{{ score.subject_name }}</td>
                  <td>{{ score.chapter_name }}</td>
                  <td>{{ score.quiz_title }}</td>
                  <td><span class="badge bg-success">{{ score.score }}</span></td>
                  <td>{{ score.total_possible_marks }}</td>
                  <td>{{ score.percentage }}%</td>
                  <td>
                    <span class="badge" :class="score.grade === 'Excellent' ? 'bg-success' : 'bg-warning text-dark'">
                      {{ score.grade }}
                    </span>
                  </td>
                  <td>{{ score.date_taken }}</td>
                </tr>
                <tr v-if="filteredScores.length === 0">
                  <td colspan="8" class="text-muted">No scores found for your search.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="text-center mt-4">
            <button class="btn btn-outline-primary" @click="exportCSV">
              <i class="fas fa-file-csv me-2"></i>Export to CSV
            </button>
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
      fetch('http://127.0.0.1:5000/user_results', {
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
    fetchUsername() {
      fetch('http://127.0.0.1:5000/user/profile', {
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
      fetch('http://127.0.0.1:5000/export_details', {
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
