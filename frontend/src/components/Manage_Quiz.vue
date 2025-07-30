// managequiz.vue

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3">
          <i class="fas fa-user-circle me-2"></i>Welcome, {{ adminName }}
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
              <router-link class="nav-link" to="/admin_summary"><i class="fas fa-chart-bar me-1"></i>Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage_subject"><i class="fas fa-clipboard-list me-1"></i>Manage Subjects</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_user"><i class="fas fa-users-cog me-1"></i>Manage Users</router-link>
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

    <div class="container mt-4 d-flex justify-content-end">
      <button class="btn btn-primary" @click="AddQuizModal">
        + Add New Quiz
      </button>
    </div>

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
              <button class="btn btn-sm btn-success" @click="openAddQuestionModal(quiz.id)">Add Question</button>
              <router-link class="btn btn-sm btn-info text-white" :to="`/view_questions/${quiz.id}`">View Questions</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

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
    <Add_Question v-if="selectedQuizIdForQuestion" 
                  :quiz-id="selectedQuizIdForQuestion" 
                  @question-added="handleQuestionAdded" />
  </div>
</template>

<script>
import * as bootstrap from 'bootstrap'; 
// CHANGE 3: Import the Add_Question component (ensure correct path if different)
import Add_Question from '@/components/Add_Question.vue'; // Adjust path if needed

export default {
  // CHANGE 4: Register the Add_Question component
  components: {
    Add_Question 
  },
  data() {
    return {
      quizzes: [],
      chapters: [],
      username: '', // You might need to populate this, e.g., from localStorage
      searchQuery: '', 
      newQuiz: {
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        Is_active: true,
        date: '',
        single_attempt: false
      },
      adminName:'',
      SelectedQuiz: {
        id: null,
        chapter_id: '',
        title: '',
        description: '',
        time_limit: '',
        Is_active: true,
        date: '',
        single_attempt: false
      },
      // CHANGE 5: New data property to store the quiz ID for the Add Question modal
      selectedQuizIdForQuestion: null 
    };
  },
  computed: {
    filtered_Quizzes() {
      const query = this.quizSearch ? this.quizSearch.toLowerCase() : '';
      return this.quizzes.filter(quiz =>
        (quiz.name && quiz.name.toLowerCase().includes(query)) ||
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
    editQuizModal(quiz) {
      this.SelectedQuiz.id = quiz.id;
      this.SelectedQuiz.chapter_id = quiz.chapter_id;
      this.SelectedQuiz.title = quiz.title;
      this.SelectedQuiz.description = quiz.description;
      this.SelectedQuiz.time_limit = quiz.time_limit;
      // Ensure date is formatted for input type="date"
      this.SelectedQuiz.date = quiz.date ? new Date(quiz.date).toISOString().split('T')[0] : '';
      this.SelectedQuiz.Is_active = typeof quiz.Is_active === 'string' ? (quiz.Is_active === 'true') : !!quiz.Is_active;
      this.SelectedQuiz.single_attempt = !!quiz.single_attempt;
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).show();
    },
    editQuiz() {
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
        bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).hide();
      })
      .catch(error => {
        console.error('Error updating quiz:', error);
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
      .then(response => response.json())
      .then(data => {
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
    addQuiz() {
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
        bootstrap.Modal.getOrCreateInstance(document.getElementById('addQuizModal')).hide();
      })
      .catch(error => {
        console.error('Error adding quiz:', error);
      });
    },
    deleteQuiz(id) {
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
      .then(response => response.json())
      .then(data => {
        this.chapters = data;
        console.log("Chapters loaded:", this.chapters);
      })
      .catch(error => {
        console.error('Error fetching chapters:', error);
      });
    },
    openAddQuestionModal(quizId) {
      this.selectedQuizIdForQuestion = quizId; // Set the quiz ID to pass to the modal
      this.$nextTick(() => {
        const addQuestionModalInstance = new bootstrap.Modal(document.getElementById('addQuestionModal'));
        addQuestionModalInstance.show();
      });
    },
    handleQuestionAdded(message) {
      alert(message); // Display the message received from the modal
      this.fetchQuizzes(); // Refresh the quiz list, perhaps to update question count
      const addQuestionModalInstance = bootstrap.Modal.getInstance(document.getElementById('addQuestionModal'));
      if (addQuestionModalInstance) {
        addQuestionModalInstance.hide();
      }
      this.selectedQuizIdForQuestion = null; 
    },
    async getAdminName() {
    try {
      const res = await fetch('http://127.0.0.1:5000/admin/profile', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      });
      const data = await res.json();
      if (res.ok) {
        this.adminName = data.username;
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
    this.fetchChapters();
    this.getAdminName();
    
  }
}
</script>