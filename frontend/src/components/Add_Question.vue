<template>
  <div>
    <div class="modal fade" id="addQuestionModal" tabindex="-1" aria-labelledby="addQuestionModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addQuestionModalLabel">Add Question (for Quiz ID: {{ quizId }})</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addQuestion">
              <div class="mb-3">
                <label for="question_tag" class="form-label">Question Tag</label>
                <input type="text" class="form-control" id="question_tag" v-model="newQuestion.question_tag" />
              </div>
              <div class="mb-3">
                <label for="question_state" class="form-label">Question Statement</label>
                <textarea class="form-control" id="question_state" rows="3" v-model="newQuestion.question_state"></textarea>
              </div>
              <div class="mb-3">
                <label for="option_1" class="form-label">Option 1</label>
                <input type="text" class="form-control" id="option_1" v-model="newQuestion.option_1" />
              </div>
              <div class="mb-3">
                <label for="option_2" class="form-label">Option 2</label>
                <input type="text" class="form-control" id="option_2" v-model="newQuestion.option_2" />
              </div>
              <div class="mb-3">
                <label for="option_3" class="form-label">Option 3</label>
                <input type="text" class="form-control" id="option_3" v-model="newQuestion.option_3" />
              </div>
              <div class="mb-3">
                <label for="option_4" class="form-label">Option 4</label>
                <input type="text" class="form-control" id="option_4" v-model="newQuestion.option_4" />
              </div>
              <div class="mb-3">
                <label for="correct_answer" class="form-label">Correct Answer</label>
                <select class="form-select" id="correct_answer" v-model="newQuestion.correct_answer">
                    <option value="">Select Correct Option</option>
                    <option value="option_1">{{ newQuestion.option_1 || 'Option 1' }}</option>
                    <option value="option_2">{{ newQuestion.option_2 || 'Option 2' }}</option>
                    <option value="option_3">{{ newQuestion.option_3 || 'Option 3' }}</option>
                    <option value="option_4">{{ newQuestion.option_4 || 'Option 4' }}</option>
                </select>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Add Question</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// CHANGE 4: Import Bootstrap if you directly use Bootstrap JS APIs (like Modal class).
// If your main.js or App.vue makes Bootstrap globally available, this might be optional.
import * as bootstrap from 'bootstrap'; 

export default {
  // CHANGE 5: Accept quizId as a prop from the parent component (managequiz.vue)
  // This replaces this.$route.params.quiz_id
  props: {
    quizId: {
      type: [Number, String], // Allow number or string, based on your backend ID type
      required: true // The quizId is essential for adding a question
    }
  },
  data() {
    return {
      newQuestion: {
        question_tag: '',
        question_state: '',
        option_1: '',
        option_2: '',
        option_3: '',
        option_4: '',
        correct_answer: '',
      },
    };
  },
  methods: {
    async addQuestion() { // CHANGE 6: Use async/await for cleaner fetch handling
      // Use the quizId prop for the API endpoint
      const url = `http://127.0.0.1:5000/add_question/${this.quizId}`;
      // Get the authentication token
      const token = localStorage.getItem('admin_token'); // Make sure this is the correct key!

      // Basic client-side validation for the token
      if (!token) {
        alert('Authentication token is missing. Please log in again.');
        // Optionally, you might want to emit an event to tell the parent to redirect to login
        // this.$emit('auth-error'); 
        return;
      }

      // Basic client-side validation for form fields
      // You can add more comprehensive validation here if needed
      if (!this.newQuestion.question_tag || !this.newQuestion.question_state ||
          !this.newQuestion.option_1 || !this.newQuestion.option_2 ||
          !this.newQuestion.option_3 || !this.newQuestion.option_4 ||
          !this.newQuestion.correct_answer) {
        alert('Please fill in all question and option fields.');
        return;
      }

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token // Correctly send the token
          },
          body: JSON.stringify(this.newQuestion),
        });

        const data = await response.json();

        // Check for success based on HTTP status code
        if (response.ok) { // `response.ok` is true for 2xx status codes
          alert(data.message || 'Question added successfully!');
          // CHANGE 7: Emit an event to the parent component (manage_quiz.vue)
          // The parent will handle closing the modal and potentially refreshing its data.
          this.$emit('question-added', data.message || 'Question added successfully!');

          // Reset the form fields for the next question (good UX for a modal)
          this.newQuestion = {
            question_tag: '',
            question_state: '',
            option_1: '',
            option_2: '',
            option_3: '',
            option_4: '',
            correct_answer: '',
          };
          // Optional: Programmatically close the modal here, though parent usually handles it
          // const modalElement = document.getElementById('addQuestionModal');
          // const modalInstance = bootstrap.Modal.getInstance(modalElement);
          // if (modalInstance) modalInstance.hide();

        } else {
          // Handle API errors (e.g., 400 Bad Request, 401 Unauthorized, 422 Unprocessable Entity)
          const errorMessage = data.msg || data.error || 'Failed to add question. Please check server logs.';
          alert('Error adding question: ' + errorMessage);
          console.error('API Error Response:', data); // Log full error for debugging
        }
      } catch (error) {
        // Handle network errors (e.g., server unreachable, no internet)
        console.error('Network error during addQuestion:', error);
        alert('An error occurred while connecting to the server. Please try again.');
      }
    },
  },
  // CHANGE 8: Add a watch property to reset the form if quizId changes (e.g., if the modal is reused)
  watch: {
    quizId(newVal) {
      if (newVal) {
        // Reset form when a new quizId is received
        this.newQuestion = {
          question_tag: '',
          question_state: '',
          option_1: '',
          option_2: '',
          option_3: '',
          option_4: '',
          correct_answer: '',
        };
      }
    }
  }
};
</script>

<style scoped>
/* CHANGE 9: Remove any previous styling that made this component look like a full page. */
/* The Bootstrap modal classes handle the layout and appearance. */
/* For example, remove these if they were present: */
/* .container { max-width: 800px; } */
/* .card, .card-header etc. should be handled by Bootstrap classes directly */
.modal-footer {
    border-top: 1px solid #dee2e6; /* Ensure footer border if not present */
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    justify-content: flex-end;
}
</style>