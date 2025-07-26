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
              <li class="list-group-item">🔹 {{ question.option_1 }}</li>
              <li class="list-group-item">🔹 {{ question.option_2 }}</li>
              <li class="list-group-item">🔹 {{ question.option_3 }}</li>
              <li class="list-group-item">🔹 {{ question.option_4 }}</li>
            </ul>
            <p class="text-success fw-semibold">
              ✅ Correct Answer: {{ question.correct_answer }}
            </p>
            <div class="d-flex justify-content-end mt-3 gap-2">
              <button
                class="btn btn-sm btn-outline-primary"
                @click="editQuestion(question)"
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
  </div>
</template>


<script>
export default {
  data() {
  return {
    quiz: null,
    questions: []
  };
},
  
  methods: {
    
    editQuestion(question) {
  
    },

    fetchQuestions() {
  fetch(`http://127.0.0.1:5000/get_questions/${this.$route.params.quiz_id}`, {
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
      
    },
  },
  mounted(){
    this.fetchQuestions();
  },
};
</script>
