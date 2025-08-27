 <template>
  <div class="container py-4">
    <!-- Quiz Title -->
    <div class="text-center mb-5">
      <h1 v-if="quiz" class="display-5 fw-bold text-primary">{{ quiz.title }}</h1>
      <h1 v-else class="display-6 text-danger">Loading Quiz...</h1>
      <p class="lead text-muted">Below are all questions for this quiz.</p>
    </div>

    <!-- No Questions -->
    <div v-if="questions.length === 0" class="alert alert-warning text-center">
      ❗ No questions found for this quiz.
    </div>

    <!-- Questions List -->
    <div v-else class="row">
      <div
        v-for="question in questions"
        :key="question.id"
        class="col-md-6 mb-4"
      >
        <div class="card shadow-lg border-0 h-100">
          <div class="card-body">
            <h5 class="card-title fw-semibold text-dark mb-3">
              📝 {{ question.question_tag }}
            </h5>
            <p><strong>📌 Statement:</strong> {{ question.question_state }}</p>
            <ul class="list-group mb-3">
              <li class="list-group-item">🔹 1. {{ question.option_1 }}</li>
              <li class="list-group-item">🔹 2.{{ question.option_2 }}</li>
              <li class="list-group-item">🔹 3. {{ question.option_3 }}</li>
              <li class="list-group-item">🔹 4. {{ question.option_4 }}</li>
            </ul>
            <p class="text-success fw-semibold">
              ✅ Correct Answer: {{ question['option_' + question.correct_answer.slice(-1)] || 'N/A' }}
            </p>
            <div class="d-flex justify-content-end mt-3 gap-2">
              <button
                class="btn btn-sm btn-outline-primary"
                @click="editQuestionModal(question)"
              >
                ✏️ Edit
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="deleteQuestion(question.id)"
              >
                🗑️ Delete
              </button>
            </div>
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
export default {
  data() {
  return {
    quiz: null,
    questions: [],
    SelectedQuestion:{
      id: null,
      question_tag: '',
      question_state: '',
      option_1: '',
      option_2: '',
      option_3: '',
      option_4: '',
      correct_answer: ''
    }
  };
},
  
  methods: {
    
    editQuestionModal(question) {
      this.SelectedQuestion = question;
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuestionModal')).show();
        
    },
    editQuestion(){
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_question/${this.SelectedQuestion.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.SelectedQuestion)
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuestionModal')).hide();
        this.fetchQuestions();
      });
      
    },

    fetchQuestions() {
    fetch(`https://quiz-app-v2-py9b.onrender.com/get_questions/${this.$route.params.quiz_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": 'Bearer ' + localStorage.getItem('admin_token')
    },
  })
  .then(response => response.json())
  .then(data => {
    this.questions = data.questions;
    this.quiz = data.quiz;
  })
  .catch(error => {
    console.error("Failed to fetch quiz data", error);
  });
},
    deleteQuestion(id) {
      if (!confirm("Are you sure you want to delete this question?")) {
        return;
      }
      fetch(`https://quiz-app-v2-py9b.onrender.com/delete_question/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authorization": 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchQuestions();
      })
      .catch(error => {
        console.error("Failed to delete question", error);
      })
    },
  },
  mounted(){
    this.fetchQuestions();
  },
};
</script>
