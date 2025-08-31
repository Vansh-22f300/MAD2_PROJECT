<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">Admin Panel</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-link"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/admin_summary" class="nav-link"><i class="fas fa-chart-bar me-2"></i>Summary</router-link>
        <router-link to="/manage_quiz" class="nav-link active"><i class="fas fa-clipboard-list me-2"></i>Manage Quizzes</router-link>
        <router-link to="/admin_user" class="nav-link"><i class="fas fa-users-cog me-2"></i>Manage Users</router-link>
        <router-link to="/manage_subject" class="nav-link"><i class="fas fa-book me-2"></i>Manage Subjects</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <div>
          <h2 class="fw-bold">Manage Quizzes</h2>
          <p class="text-muted">Create, edit, and organize all quizzes.</p>
        </div>
        <div class="d-flex align-items-center gap-3">
            <div class="search-wrapper">
              <i class="fas fa-search search-icon"></i>
              <input class="form-control" type="search" placeholder="Search quizzes..." v-model="searchQuery" />
            </div>
            <button class="btn btn-primary-custom" @click="AddQuizModal">
              <i class="fas fa-plus me-2"></i>Add Quiz
            </button>
        </div>
      </header>

      <section class="mt-4">
        <div class="data-card">
          <div v-if="!quizzes || quizzes.length === 0" class="text-center p-5">
            <i class="fas fa-box-open fa-2x text-muted mb-3"></i>
            <p class="lead text-muted">No quizzes have been created yet.</p>
          </div>

          <div class="table-responsive" v-else>
            <table class="table modern-table">
              <thead>
                <tr>
                  <th>Quiz Title</th>
                  <th>Subject & Chapter</th>
                  <th>Status</th>
                  <th>Duration</th>
                  <th class="text-center">Questions</th>
                  <th class="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                  
                  <td>
                    <div class="fw-bold">{{ quiz.title }}</div>
                    <small class="text-muted">{{ quiz.description }}</small>
                  </td>
                  <td>
                    <div class="fw-bold">{{ quiz.subject_name }}</div>
                    <small class="text-muted">{{ quiz.chapter_name }}</small>
                  </td>
                  <td>
                    <span class="badge status-badge" :class="quiz.Is_active ? 'active' : 'inactive'">
                      {{ quiz.Is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>{{ quiz.time_limit }} min</td>
                  <td class="text-center">
                      <button class="btn btn-sm btn-outline-info" @click="openViewQuestionsModal(quiz)">
                      View
                    </button>
                  </td>
                  <td class="text-end">
                    <button class="btn btn-sm btn-outline-success me-2" @click="openAddQuestionModal(quiz.id)" title="Add Question">
                      <i class="fas fa-plus"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-primary me-2" @click="editQuizModal(quiz)" title="Edit Quiz">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="deleteQuiz(quiz.id)" title="Delete Quiz">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
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
    <div class="modal fade" id="viewQuestionsModal" tabindex="-1">
  <div class="modal-dialog modal-lg modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">
          <i class="fas fa-list-ol me-2"></i>Questions for "{{ selectedQuizForView ? selectedQuizForView.title : '' }}"
        </h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <div v-if="loadingQuestions" class="text-center p-5">
          <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
        </div>
        <div v-else-if="viewedQuestions.length === 0" class="alert alert-info">
          No questions have been added to this quiz yet.
        </div>
        <ul class="list-group list-group-flush question-list" v-else>
          <li v-for="(question, index) in viewedQuestions" :key="question.id" class="list-group-item">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <div class="fw-bold mb-2">{{ index + 1 }}. {{ question.question_state }}</div>
                <ul class="list-unstyled ps-3 options-list">
                  <li :class="{ 'correct-answer': 'option_1' === question.correct_answer }">
                    <i class="fas me-2" :class="'option_1' === question.correct_answer ? 'fa-check-circle' : 'fa-circle'"></i>
                    {{ question.option_1 }}
                  </li>
                  <li :class="{ 'correct-answer': 'option_2' === question.correct_answer }">
                    <i class="fas me-2" :class="'option_2' === question.correct_answer ? 'fa-check-circle' : 'fa-circle'"></i>
                    {{ question.option_2 }}
                  </li>
                  <li :class="{ 'correct-answer': 'option_3' === question.correct_answer }">
                    <i class="fas me-2" :class="'option_3' === question.correct_answer ? 'fa-check-circle' : 'fa-circle'"></i>
                    {{ question.option_3 }}
                  </li>
                  <li :class="{ 'correct-answer': 'option_4' === question.correct_answer }">
                    <i class="fas me-2" :class="'option_4' === question.correct_answer ? 'fa-check-circle' : 'fa-circle'"></i>
                    {{ question.option_4 }}
                  </li>
                </ul>
              </div>
              <div class="d-flex gap-2 flex-shrink-0 ms-3">
                <button class="btn btn-sm btn-outline-primary" @click="openEditQuestionModal(question)">Edit</button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteQuestionFromModal(question.id)">Delete</button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
    <!-- Edit Question Modal -->
    <div class="modal fade" id="editQuestionModal" tabindex="-1" aria-labelledby="editQuestionModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editQuestionModalLabel">Edit Question</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editQuestion">
              <div class="mb-3">
                <label for="question_tag" class="form-label">Question Tag</label>
                <input type="text" class="form-control" id="question_tag" v-model="SelectedQuestion.question_tag" />
              </div>
              <div class="mb-3">
                <label for="question_state" class="form-label">Question Statement</label>
                <textarea class="form-control" id="question_state" rows="3" v-model="SelectedQuestion.question_state"></textarea>
              </div>
              <div class="mb-3">
                <label for="option_1" class="form-label">Option 1</label>
                <input type="text" class="form-control" id="option_1" v-model="SelectedQuestion.option_1" />
              </div>
              <div class="mb-3">
                <label for="option_2" class="form-label">Option 2</label>
                <input type="text" class="form-control" id="option_2" v-model="SelectedQuestion.option_2" />
              </div>
              <div class="mb-3">
                <label for="option_3" class="form-label">Option 3</label>
                <input type="text" class="form-control" id="option_3" v-model="SelectedQuestion.option_3" />
              </div>
              <div class="mb-3">
                <label for="option_4" class="form-label">Option 4</label>
                <input type="text" class="form-control" id="option_4" v-model="SelectedQuestion.option_4" />
              </div>
              <div class="mb-3">
                <label for="correct_answer" class="form-label">Correct Answer</label>
                <select class="form-select" id="correct_answer" v-model="SelectedQuestion.correct_answer">
                  <option value="">Select Correct Option</option>
                  <option value="option_1">{{ SelectedQuestion.option_1 || 'Option 1' }}</option>
                  <option value="option_2">{{ SelectedQuestion.option_2 || 'Option 2' }}</option>
                  <option value="option_3">{{ SelectedQuestion.option_3 || 'Option 3' }}</option>
                  <option value="option_4">{{ SelectedQuestion.option_4 || 'Option 4' }}</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>              
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
      selectedQuizIdForQuestion: null ,
      // Data for View/Edit Questions Modal
      viewQuestionsModalInstance: null,
      editQuestionModalInstance: null,
      selectedQuizForView: null,
      viewedQuestions: [],
      loadingQuestions: false,
      SelectedQuestion: {},
    };
  },
  computed: {
    // --- THIS IS THE UPDATED SEARCH LOGIC ---
    filteredQuizzes() {
      // If there's no search query, return all quizzes
      if (!this.searchQuery) {
        return this.quizzes;
      }
      
      const query = this.searchQuery.toLowerCase().trim();
      
      return this.quizzes.filter(quiz => {
        // Check for matches in quiz name, subject name, or chapter name
        const quizNameMatch = quiz.title && quiz.title.toLowerCase().includes(query);
        const subjectNameMatch = quiz.subject_name && quiz.subject_name.toLowerCase().includes(query);
        const chapterNameMatch = quiz.chapter_name && quiz.chapter_name.toLowerCase().includes(query);
        
        return quizNameMatch || subjectNameMatch || chapterNameMatch;
      });
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
      this.SelectedQuiz.date = quiz.date ? new Date(quiz.date).toISOString().split('T')[0] : '';
      this.SelectedQuiz.Is_active = typeof quiz.Is_active === 'string' ? (quiz.Is_active === 'true') : !!quiz.Is_active;
      this.SelectedQuiz.single_attempt = !!quiz.single_attempt;
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).show();
    },
    editQuiz() {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_quiz/${this.SelectedQuiz.id}`, {
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
      fetch('https://quiz-app-v2-py9b.onrender.com/get_quiz', {
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
      fetch('https://quiz-app-v2-py9b.onrender.com/add_quiz', {
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
      fetch(`https://quiz-app-v2-py9b.onrender.com/delete_quiz/${id}`, {
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
      fetch('https://quiz-app-v2-py9b.onrender.com/add_chapter/get', {
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
    openViewQuestionsModal(quiz) {
      this.selectedQuizForView = quiz;
      this.fetchQuestionsForModal(quiz.id);
      this.viewQuestionsModalInstance.show();
    },
    async fetchQuestionsForModal(quizId) {
      this.loadingQuestions = true;
      try {
        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/get_questions/${quizId}`, {
          headers: { 'Authorization': 'Bearer ' + localStorage.getItem('admin_token') }
        });
        const data = await response.json();
        this.viewedQuestions = data.questions || [];
      } catch (error) {
        console.error("Error fetching questions:", error);
      } finally {
        this.loadingQuestions = false;
      }
    },
    openEditQuestionModal(question) {
      this.SelectedQuestion = { ...question };
      this.editQuestionModalInstance.show();
    },
    async editQuestion() {
      try {
        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/edit_question/${this.SelectedQuestion.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json", "Authorization": 'Bearer ' + localStorage.getItem('admin_token') },
          body: JSON.stringify(this.SelectedQuestion)
        });
        const data = await response.json();
        alert(data.message);
        if (response.ok) {
          this.editQuestionModalInstance.hide();
          this.fetchQuestionsForModal(this.selectedQuizForView.id); // Refresh the list
        }
      } catch (error) {
        console.error("Error editing question:", error);
      }
    },
    async deleteQuestionFromModal(questionId) {
      if (!confirm("Are you sure?")) return;
      try {
        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/delete_question/${questionId}`, {
          method: "DELETE",
          headers: { 'Authorization': 'Bearer ' + localStorage.getItem('admin_token') }
        });
        const data = await response.json();
        alert(data.message);
        if (response.ok) {
          this.fetchQuestionsForModal(this.selectedQuizForView.id); // Refresh the list
        }
      } catch (error) {
        console.error("Error deleting question:", error);
      }
    },
    async getAdminName() {
    try {
      const res = await fetch('https://quiz-app-v2-py9b.onrender.com/admin/profile', {
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
    this.viewQuestionsModalInstance = new bootstrap.Modal(document.getElementById('viewQuestionsModal'));
    this.editQuestionModalInstance = new bootstrap.Modal(document.getElementById('editQuestionModal'));
    
  }
}
</script>