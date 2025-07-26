<template> 
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3">
          <i class="fas fa-user-circle me-2"></i>Welcome, {{ username }}
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin"><i class="fas fa-home me-1"></i>Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/summary"><i class="fas fa-chart-bar me-1"></i>Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/manage_quiz"><i class="fas fa-clipboard-list me-1"></i>Manage Quizzes</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/manage_user"><i class="fas fa-users-cog me-1"></i>Manage Users</router-link>
            </li>
          </ul>
          <form class="d-flex me-3" @submit.prevent>
            <div class="input-group">
              <input class="form-control" type="search" placeholder="Search..." v-model="searchQuery">
              <button class="btn btn-light" type="submit"><i class="fas fa-search"></i></button>
            </div>
          </form>
          <router-link to="/login" class="btn btn-outline-light"><i class="fas fa-sign-out-alt me-1"></i>Logout</router-link>
        </div>
      </div>
    </nav>

    <!-- Add Quiz Button -->
    <div class="container mt-4 d-flex justify-content-end">
      <button class="btn btn-primary" @click="AddQuizModal">
        + Add New Quiz
      </button>
    </div>

    <!-- Quiz Cards -->
    <div class="container mt-4">
      <div class="row">
        <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 col-lg-4 mb-4">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-body">
              <h5 class="card-title">{{ quiz.name }}</h5>
              <p class="card-text text-muted mb-1">📘 <strong>Subject:</strong> {{ quiz.subject_name }}</p>
              <p class="card-text text-muted mb-1">📖 <strong>Chapter:</strong> {{ quiz.chapter_name }}</p>
              <p class="card-text text-muted mb-1">🕒 <strong>Duration:</strong> {{ quiz.time_limit }} minutes</p>
              <p class="card-text text-muted mb-1">🔒 <strong>Single Attempt:</strong> {{ quiz.single_attempt ? 'Yes' : 'No' }}</p>
              <p class="card-text">{{ quiz.description }}</p>
              <div class="d-flex justify-content-between mt-3">
                <button class="btn btn-sm btn-primary me-2" @click="editQuizModal(quiz)">
                  <i class="fas fa-edit me-1"></i>Edit
                </button>
                
                <button class="btn btn-sm btn-danger" @click="deleteQuiz(quiz.id)">
                  <i class="fas fa-trash me-1"></i>Delete
                </button>
              </div>
            </div>
            <div class="card-footer bg-white border-0 d-flex justify-content-between">
              <router-link class="btn btn-sm btn-success" :to="`/add_question/${quiz.id}`">Add Question</router-link>
              <router-link class="btn btn-sm btn-info text-white" :to="`/view_questions/${quiz.id}`">View Questions</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Quiz Modal -->
    <div class="modal fade" id="addQuizModal" tabindex="-1" aria-labelledby="addQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content shadow">
          <div class="modal-header">
            <h5 class="modal-title" id="addQuizModalLabel">Add New Quiz</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form submit.prevent="addQuiz">
              <div class="mb-3">
                <label for="quiz-title" class="form-label">Quiz Title</label>
                <input type="text" class="form-control" id="quiz-title" v-model="newQuiz.title" required>
              </div>
              <div class="mb-3">
                <label for="quiz-description" class="form-label">Quiz Description</label>
                <input type="text" class="form-control" id="quiz-description" v-model="newQuiz.description" required>
              </div>
              <div class="mb-3">
                <label for="quiz-time_limit" class="form-label">Quiz Duration (minutes)</label>
                <input type="text" class="form-control" id="quiz-time_limit" v-model="newQuiz.time_limit" required>
              </div>
              <div class="mb-3">
                <label for="quiz-chapter" class="form-label">Chapter</label>
                <select class="form-select" id="quiz-chapter" v-model="newQuiz.chapter_id" required>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
                </select>

              </div>
              <div class="mb-3">
                <label for="quiz-date" class="form-label">Quiz Date</label>
                <input type="date" class="form-control" id="quiz-date" v-model="newQuiz.date" required>
              </div>
              <div class="mb-3">
                <label for="quiz-active" class="form-label">Is Active</label>
                <select class="form-select" id="quiz-active" v-model="newQuiz.Is_active" required>
                  <option :value="true">Yes</option>
                  <option :value="false">No</option>
                </select>

              </div>
              <div class="mb-3">
                    <label for="single-attempt" class="form-label">Single Attempt</label>
                    <input type="checkbox" id="single-attempt" v-model="newQuiz.single_attempt">
                </div>

            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="addQuiz">Add Quiz</button>
          </div>
        </div>
      </div>
    </div>
    <!-- Edit Quiz Modal -->
    <div class="modal fade" id="editQuizModal" tabindex="-1" aria-labelledby="editQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content shadow">
          <div class="modal-header">
            <h5 class="modal-title" id="editQuizModalLabel">Edit Quiz</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editQuiz">
              <div class="mb-3">
                <label for="edit-quiz-name" class="form-label">Quiz Name</label>
                <input type="text" class="form-control" id="edit-quiz-name" v-model="SelectedQuiz.title" required>
              </div>
              <div class="mb-3">
                <label for="edit-quiz-description" class="form-label">Quiz Description</label>
                <input type="text" class="form-control" id="edit-quiz-description" v-model="SelectedQuiz.description" required>
              </div>
              <div class="mb-3">
                <label for="edit-quiz-time_limit" class="form-label">Quiz Duration (minutes)</label>
                <input type="text" class="form-control" id="edit-quiz-time_limit" v-model="SelectedQuiz.time_limit" required>
              </div>
              <div class="mb-3">
                <label for="edit-quiz-chapter" class="form-label">Chapter</label>
                <select class="form-select" id="edit-quiz-chapter" v-model="SelectedQuiz.chapter_id" required>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="edit-quiz-date" class="form-label">Quiz Date</label>
                <input type="date" class="form-control" id="edit-quiz-date" v-model="SelectedQuiz.date" required>
              </div>
              <div class="mb-3">
                <label for="edit-quiz-active" class="form-label">Is Active</label>
                <select class="form-select" id="edit-quiz-active" v-model="SelectedQuiz.Is_active" required>
                <option :value="true">Yes</option>
                <option :value="false">No</option>
              </select>

              </div>
              <div class="mb-3">
                <label for="edit-single-attempt" class="form-label">Single Attempt</label>
                <input type="checkbox" id="edit-single-attempt" v-model="SelectedQuiz.single_attempt">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="editQuiz">Save Changes</button>
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
      quizzes: [],
      chapters: [],
      newQuiz: {
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        Is_active: true,
        date: '',
        single_attempt: false
      },
      quizSearch: '', // Retained your original variable name

      SelectedQuiz: {
        id: null,
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        // Initialize Is_active as a boolean, not a string
        Is_active: true, // Changed from 'true' to true
        date: '',
        single_attempt: false
      }
    };
  },
  computed: {
    filtered_Quizzes() {
      // Use quizSearch for filtering as per your original code
      const query = this.quizSearch ? this.quizSearch.toLowerCase() : '';
      return this.quizzes.filter(quiz =>
        (quiz.name && quiz.name.toLowerCase().includes(query)) ||
        (quiz.subject_name && quiz.subject_name.toLowerCase().includes(query))
      );
    }
  },
  methods: {
    AddQuizModal() {
      // Reset newQuiz to default values when opening the modal
      this.newQuiz = {
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        Is_active: true, // Default to true for new quizzes
        date: '',
        single_attempt: false
      };
      // Retained your original Bootstrap modal call
      bootstrap.Modal.getOrCreateInstance(document.getElementById('addQuizModal')).show();
    },
    editQuizModal(quiz) {
      this.SelectedQuiz.id = quiz.id;
      this.SelectedQuiz.chapter_id = quiz.chapter_id;
      this.SelectedQuiz.title = quiz.title;
      this.SelectedQuiz.description = quiz.description;
      this.SelectedQuiz.time_limit = quiz.time_limit;
      this.SelectedQuiz.date = quiz.date;
      // Convert Is_active to boolean: if it's a string 'true', make it true; otherwise, use !! to convert to boolean
      this.SelectedQuiz.Is_active = typeof quiz.Is_active === 'string' ? (quiz.Is_active === 'true') : !!quiz.Is_active;
      // Ensure single_attempt is a boolean
      this.SelectedQuiz.single_attempt = !!quiz.single_attempt;
      // Retained your original Bootstrap modal call
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).show();
    },
    editQuiz() {
      // Retained your original fetch structure and error handling
      fetch(`http://127.0.0.1:5000/edit_quiz/${this.SelectedQuiz.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.SelectedQuiz)
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message || 'Quiz updated successfully!');
        this.fetchQuizzes();
        // Retained your original Bootstrap modal call
        bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).hide();
      })
      .catch(error => {
        console.error('Error updating quiz:', error);
        // Retained your original error message style
      });
    },
    fetchQuizzes() {
      // Retained your original fetch structure and error handling
      fetch('http://127.0.0.1:5000/get_quiz', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        // Map fetched data to ensure Is_active and single_attempt are booleans
        this.quizzes = data.map(quiz => ({
          ...quiz,
          Is_active: typeof quiz.Is_active === 'string' ? (quiz.Is_active === 'true') : !!quiz.Is_active,
          single_attempt: !!quiz.single_attempt
        }));
      })
      .catch(error => {
        console.error('Error fetching quizzes:', error);
        // Retained your original error message style
      });
    },
    addQuiz() {
      // Retained your original fetch structure and error handling
      fetch('http://127.0.0.1:5000/add_quiz', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.newQuiz)
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message || 'Quiz added successfully!');
        this.fetchQuizzes();
        // Retained your original Bootstrap modal call
        bootstrap.Modal.getOrCreateInstance(document.getElementById('addQuizModal')).hide();
      })
      .catch(error => {
        console.error('Error adding quiz:', error);
        // Retained your original error message style
      });
    },
    deleteQuiz(id) {
      // Retained your original confirm dialog and fetch structure
      if (!confirm("Are you sure you want to delete this quiz?")) {
        return;
      }
      fetch(`http://127.0.0.1:5000/delete_quiz/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message || 'Quiz deleted successfully!');
        this.fetchQuizzes();
      })
      .catch(error => {
        console.error('Error deleting quiz:', error);
        this.showMessage('Error', 'Failed to delete quiz: ' + error.message); // Retained your original showMessage call
      });
    },
    fetchChapters() {
      // Retained your original fetch structure and error handling
      fetch('http://127.0.0.1:5000/add_chapter/get', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
      })
      .then(response => response.json())
      .then(data => {
        this.chapters = data;
        console.log("Chapters loaded:", this.chapters);
      })
      .catch(error => {
        console.error('Error fetching chapters:', error);
        // Retained your original error message style
      });
    },
  },

  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  }
}
</script>