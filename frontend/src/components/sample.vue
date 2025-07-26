
<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm py-3">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3 fs-5">
          <i class="fas fa-user-circle me-2"></i>Welcome, {{ username }}
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin"><i class="fas fa-home me-2"></i>Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/summary"><i class="fas fa-chart-bar me-2"></i>Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/manage_quiz"><i class="fas fa-clipboard-list me-2"></i>Manage Quizzes</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/manage_user"><i class="fas fa-users-cog me-2"></i>Manage Users</router-link>
            </li>
          </ul>
          <form class="d-flex me-3" @submit.prevent>
            <div class="input-group">
              <input class="form-control" type="search" placeholder="Search quizzes..." v-model="searchQuery" aria-label="Search">
              <button class="btn btn-light" type="submit"><i class="fas fa-search"></i></button>
            </div>
          </form>
          <router-link to="/login" class="btn btn-outline-light"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
        </div>
      </div>
    </nav>

    <div class="container py-5">
      <!-- Add Quiz Button -->
      <div class="d-flex justify-content-end mb-4">
        <button class="btn btn-primary btn-lg shadow-sm" @click="AddQuizModal">
          <i class="fas fa-plus-circle me-2"></i>Add New Quiz
        </button>
      </div>

      <!-- Quiz Cards -->
      <div class="row">
        <div v-for="quiz in filtered_Quizzes" :key="quiz.id" class="col-md-6 col-lg-4 mb-4">
          <div class="card h-100 shadow-lg border-0 rounded-3">
            <div class="card-header bg-info text-white fw-bold fs-5 rounded-top-3 py-3">
              {{ quiz.title }}
            </div>
            <div class="card-body d-flex flex-column">
              <p class="card-text text-muted mb-1"><i class="fas fa-book-open me-2"></i><strong class="text-dark">Subject:</strong> {{ quiz.subject_name }}</p>
              <p class="card-text text-muted mb-1"><i class="fas fa-bookmark me-2"></i><strong class="text-dark">Chapter:</strong> {{ quiz.chapter_name }}</p>
              <p class="card-text text-muted mb-1"><i class="fas fa-clock me-2"></i><strong class="text-dark">Duration:</strong> {{ quiz.time_limit }} minutes</p>
              <p class="card-text mb-2">
                <i class="fas fa-toggle-on me-2"></i><strong class="text-dark">Active:</strong>
                <span :class="['badge', quiz.Is_active ? 'bg-success' : 'bg-danger']">{{ quiz.Is_active ? 'Yes' : 'No' }}</span>
              </p>
              <p class="card-text mb-2">
                <i class="fas fa-redo-alt me-2"></i><strong class="text-dark">Single Attempt:</strong>
                <span :class="['badge', quiz.single_attempt ? 'bg-warning text-dark' : 'bg-secondary']">{{ quiz.single_attempt ? 'Yes' : 'No' }}</span>
              </p>
              <p class="card-text text-secondary mt-2 flex-grow-1">{{ quiz.description }}</p>
              
              <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top">
                <button class="btn btn-sm btn-outline-primary me-2 rounded-pill px-3" @click="editQuizModal(quiz)">
                  <i class="fas fa-edit me-1"></i>Edit
                </button>
                <button class="btn btn-sm btn-outline-danger rounded-pill px-3" @click="deleteQuiz(quiz.id)">
                  <i class="fas fa-trash-alt me-1"></i>Delete
                </button>
              </div>
            </div>
            <div class="card-footer bg-light border-0 d-flex justify-content-between rounded-bottom-3 py-3">
              <router-link class="btn btn-sm btn-success rounded-pill px-3" :to="`/add_question/${quiz.id}`">
                <i class="fas fa-plus me-1"></i>Add Question
              </router-link>
              <router-link class="btn btn-sm btn-info text-white rounded-pill px-3" :to="`/view_questions/${quiz.id}`">
                <i class="fas fa-eye me-1"></i>View Questions
              </router-link>
            </div>
          </div>
        </div>
        <div v-if="filtered_Quizzes.length === 0" class="col-12 text-center py-5">
          <p class="lead text-muted">No quizzes found matching your criteria.</p>
        </div>
      </div>
    </div>

    <!-- Add Quiz Modal -->
    <div class="modal fade" id="addQuizModal" tabindex="-1" aria-labelledby="addQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content shadow-lg rounded-4">
          <div class="modal-header bg-primary text-white rounded-top-4">
            <h5 class="modal-title" id="addQuizModalLabel"><i class="fas fa-plus-circle me-2"></i>Add New Quiz</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="addQuiz">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="quiz-title" class="form-label fw-bold">Quiz Title</label>
                  <input type="text" class="form-control" id="quiz-title" v-model="newQuiz.title" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="quiz-chapter" class="form-label fw-bold">Chapter</label>
                  <select class="form-select" id="quiz-chapter" v-model="newQuiz.chapter_id" required>
                    <option value="" disabled>Select a chapter</option>
                    <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label for="quiz-description" class="form-label fw-bold">Quiz Description</label>
                <textarea class="form-control" id="quiz-description" v-model="newQuiz.description" rows="3" required></textarea>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="quiz-time_limit" class="form-label fw-bold">Quiz Duration (minutes)</label>
                  <input type="number" class="form-control" id="quiz-time_limit" v-model="newQuiz.time_limit" required min="1">
                </div>
                <div class="col-md-6 mb-3">
                  <label for="quiz-date" class="form-label fw-bold">Quiz Date</label>
                  <input type="date" class="form-control" id="quiz-date" v-model="newQuiz.date" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="quiz-active" class="form-label fw-bold">Is Active</label>
                  <select class="form-select" id="quiz-active" v-model="newQuiz.Is_active" required>
                    <option :value="true">Yes</option>
                    <option :value="false">No</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3 d-flex align-items-center pt-4">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="single-attempt" v-model="newQuiz.single_attempt">
                    <label class="form-check-label fw-bold" for="single-attempt">Single Attempt</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer rounded-bottom-4">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="addQuiz">Add Quiz</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Quiz Modal -->
    <div class="modal fade" id="editQuizModal" tabindex="-1" aria-labelledby="editQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content shadow-lg rounded-4">
          <div class="modal-header bg-info text-white rounded-top-4">
            <h5 class="modal-title" id="editQuizModalLabel"><i class="fas fa-edit me-2"></i>Edit Quiz</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="editQuiz">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="edit-quiz-title" class="form-label fw-bold">Quiz Title</label>
                  <input type="text" class="form-control" id="edit-quiz-title" v-model="SelectedQuiz.title" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="edit-quiz-chapter" class="form-label fw-bold">Chapter</label>
                  <select class="form-select" id="edit-quiz-chapter" v-model="SelectedQuiz.chapter_id" required>
                    <option value="" disabled>Select a chapter</option>
                    <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label for="edit-quiz-description" class="form-label fw-bold">Quiz Description</label>
                <textarea class="form-control" id="edit-quiz-description" v-model="SelectedQuiz.description" rows="3" required></textarea>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="edit-quiz-time_limit" class="form-label fw-bold">Quiz Duration (minutes)</label>
                  <input type="number" class="form-control" id="edit-quiz-time_limit" v-model="SelectedQuiz.time_limit" required min="1">
                </div>
                <div class="col-md-6 mb-3">
                  <label for="edit-quiz-date" class="form-label fw-bold">Quiz Date</label>
                  <input type="date" class="form-control" id="edit-quiz-date" v-model="SelectedQuiz.date" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="edit-quiz-active" class="form-label fw-bold">Is Active</label>
                  <select class="form-select" id="edit-quiz-active" v-model="SelectedQuiz.Is_active" required>
                    <option :value="true">Yes</option>
                    <option :value="false">No</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3 d-flex align-items-center pt-4">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="edit-single-attempt" v-model="SelectedQuiz.single_attempt">
                    <label class="form-check-label fw-bold" for="edit-single-attempt">Single Attempt</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer rounded-bottom-4">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="editQuiz">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Custom Message Modal -->
    <div class="modal fade" id="messageModal" tabindex="-1" aria-labelledby="messageModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-sm">
        <div class="modal-content rounded-3 shadow-sm">
          <div :class="['modal-header', messageModalTitle === 'Success' ? 'bg-primary' : 'bg-danger', 'text-white', 'rounded-top-3']">
            <h5 class="modal-title" id="messageModalTitle">Message</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" id="messageModalBody">
            <!-- Message content will be injected here -->
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Custom Confirmation Modal -->
    <div class="modal fade" id="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-sm">
        <div class="modal-content rounded-3 shadow-sm">
          <div class="modal-header bg-danger text-white rounded-top-3">
            <h5 class="modal-title" id="confirmModalTitle">Confirm Action</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" id="confirmModalBody">
            Are you sure you want to proceed?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" id="confirmActionButton">Confirm</button>
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
      searchQuery: '',
      SelectedQuiz:{
        id: null, 
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        Is_active: true,
        date: '',
        single_attempt: false
      },
      username: 'Admin',
      confirmCallback: null,
      messageModalTitle: '' // Added to dynamically set modal header color
    };
  },
  computed:{
    filtered_Quizzes() {
      const query = this.searchQuery ? this.searchQuery.toLowerCase() : '';
      return this.quizzes.filter(quiz => 
        (quiz.title && quiz.title.toLowerCase().includes(query)) ||
        (quiz.subject_name && quiz.subject_name.toLowerCase().includes(query))
      );
    }
  },
  methods: {
    AddQuizModal() {
      this.newQuiz = {
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        Is_active: true,
        date: '',
        single_attempt: false
      };
      bootstrap.Modal.getOrCreateInstance(document.getElementById('addQuizModal')).show();
    },
    editQuizModal(quiz){
      this.SelectedQuiz = { ...quiz };
      this.SelectedQuiz.Is_active = Boolean(quiz.Is_active);
      if (quiz.date) {
        this.SelectedQuiz.date = quiz.date.split('T')[0]; 
      }
      this.SelectedQuiz.single_attempt = Boolean(quiz.single_attempt);
      
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).show();
    },
    editQuiz(){
      fetch(`http://127.0.0.1:5000/edit_quiz/${this.SelectedQuiz.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.SelectedQuiz)
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.message || `HTTP error! status: ${response.status}`); });
        }
        return response.json();
      })
      .then(data => {
        this.showMessage('Success', data.message || 'Quiz updated successfully!');
        this.fetchQuizzes();
        bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).hide();
      })
      .catch(error => {
        console.error('Error updating quiz:', error);
        this.showMessage('Error', 'Failed to update quiz: ' + error.message);
      });
    },
    deleteQuiz(quizId) {
      this.showConfirm('Are you sure you want to delete this quiz?', () => {
        fetch(`http://127.0.0.1:5000/delete_quiz/${quizId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
          }
        })
        .then(response => {
          if (!response.ok) {
            return response.json().then(err => { throw new Error(err.message || `HTTP error! status: ${response.status}`); });
          }
          return response.json();
        })
        .then(data => {
          this.showMessage('Success', data.message || 'Quiz deleted successfully!');
          this.fetchQuizzes();
        })
        .catch(error => {
          console.error('Error deleting quiz:', error);
          this.showMessage('Error', 'Failed to delete quiz: ' + error.message);
        });
      });
    },
    fetchQuizzes() {
      fetch('http://127.0.0.1:5000/get_quiz', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        this.quizzes = data;
      })
      .catch(error => {
        console.error('Error fetching quizzes:', error);
        this.showMessage('Error', 'Failed to fetch quizzes: ' + error.message);
      });
    },
    addQuiz() {
      fetch('http://127.0.0.1:5000/add_quiz', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.newQuiz)
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.message || `HTTP error! status: ${response.status}`); });
        }
        return response.json();
      })
      .then(data => {
        this.showMessage('Success', data.message || 'Quiz added successfully!');
        this.fetchQuizzes();
        bootstrap.Modal.getOrCreateInstance(document.getElementById('addQuizModal')).hide();
      })
      .catch(error => {
        console.error('Error adding quiz:', error);
        this.showMessage('Error', 'Failed to add quiz: ' + error.message);
      });
    },
    deleteQuiz(id){
        fetch(`http://127.0.0.1:5000/delete_quiz/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || `HTTP error! status: ${response.status}`); });
            }
            return response.json();
        })
        .then(data => {
            this.showMessage('Success', data.message || 'Quiz deleted successfully!');
            this.fetchQuizzes();
        })
        .catch(error => {
            console.error('Error deleting quiz:', error);
            this.showMessage('Error', 'Failed to delete quiz: ' + error.message);
        });
    },
    fetchChapters() {
      fetch('http://127.0.0.1:5000/add_chapter/get', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        this.chapters = data;
      })
      .catch(error => {
        console.error('Error fetching chapters:', error);
        this.showMessage('Error', 'Failed to fetch chapters: ' + error.message);
      });
    },
    showMessage(title, message) {
      this.messageModalTitle = title; // Set the title for dynamic header color
      const messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
      document.getElementById('messageModalTitle').innerText = title;
      document.getElementById('messageModalBody').innerText = message;
      messageModal.show();
    },
    showConfirm(message, callback) {
      this.confirmCallback = callback;
      const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
      document.getElementById('confirmModalBody').innerText = message;
      document.getElementById('confirmActionButton').onclick = () => {
        if (this.confirmCallback) {
          this.confirmCallback();
        }
        confirmModal.hide();
      };
      confirmModal.show();
    }
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  }
}
</script>

