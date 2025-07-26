<template>
  <div>
    <h3 class="text-center fw-bold">Add Question</h3>
    <div class="container py-5">
            <form @submit.prevent="addQuestion">
              <div class="mb-3">
                <label for="question_tag" class="form-label">Question </label>
                <input type="text" class="form-control" id="question_tag" v-model="newQuestion.question_tag" />
              </div>
              <div class="mb-3">
                <label for="question_state" class="form-label">Question Statement</label>
                <input type="text" class="form-control" id="question_state" v-model="newQuestion.question_state" />
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
</template>

<script>

export default {
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
    addQuestion() {
        const response= fetch('http://127.0.0.1:5000/add_question/'+this.$route.params.quiz_id, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          'Authorization':'Bearer ' + localStorage.getItem('admin_token')
          },
          body: JSON.stringify(this.newQuestion),
        });
        response.then(response=>response.json())
        .then(data=>{
            if (data.message) {
                alert(data.message);
                this.$router.push('/manage_quiz/');
            }
        })
      
    },
  },
};
</script>
