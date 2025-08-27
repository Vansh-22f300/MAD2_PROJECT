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

import * as bootstrap from 'bootstrap'; 

export default {
 
  props: {
    quizId: {
      type: [Number, String], 
      required: true 
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
    async addQuestion() { 
      const url = `https://quiz-app-v2-py9b.onrender.com/add_question/${this.quizId}`;
      const token = localStorage.getItem('admin_token');

      if (!token) {
        alert('Authentication token is missing. Please log in again.');
        
        return;
      }

     
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
            'Authorization': 'Bearer ' + token 
          },
          body: JSON.stringify(this.newQuestion),
        });

        const data = await response.json();

        if (response.ok) {
          alert(data.message || 'Question added successfully!');
          
          this.$emit('question-added', data.message || 'Question added successfully!');

          this.newQuestion = {
            question_tag: '',
            question_state: '',
            option_1: '',
            option_2: '',
            option_3: '',
            option_4: '',
            correct_answer: '',
          };
         

        } else {
          const errorMessage = data.msg || data.error || 'Failed to add question. Please check server logs.';
          alert('Error adding question: ' + errorMessage);
          console.error('API Error Response:', data); // Log full error for debugging
        }
      } catch (error) {
        console.error('Network error during addQuestion:', error);
        alert('An error occurred while connecting to the server. Please try again.');
      }
    },
  },
  watch: {
    quizId(newVal) {
      if (newVal) {
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

.modal-footer {
    border-top: 1px solid #dee2e6; 
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    justify-content: flex-end;
}
</style>