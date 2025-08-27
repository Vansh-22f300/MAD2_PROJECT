<template>
  <div class="bg-light min-vh-100 d-flex flex-column">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-4 py-2">
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
      <router-link to="/login" class="btn btn-outline-light">
        <i class="fas fa-sign-out-alt me-1"></i>Logout
      </router-link>
    </nav>

    <!-- Main Content -->
    <div class="container py-5 flex-grow-1">
      <div class="row justify-content-center">
        <div class="col-lg-8">

          <!-- Header -->
          <div class="text-center mb-4">
            <h1 class="text-primary">
              <i class="fas fa-pencil-alt me-2"></i>Start Quiz
            </h1>
            <p class="text-secondary">Good luck for your quiz!</p>
          </div>

          <!-- Timer -->
          <div class="d-flex justify-content-center mb-4">
            <div class="alert alert-info rounded-pill px-4 py-2 shadow-sm">
              <i class="fas fa-clock me-2"></i>
              <strong>Time Left:</strong> {{ formatTime }}
            </div>
          </div>

          <!-- Quiz Questions -->
          <div v-if="!QuizSubmitted" class="overflow-auto">
            <form @submit.prevent="submitQuiz" class="card p-4 shadow-sm">
              <div v-for="(question, index) in questions" :key="index" class="mb-4">
                <h5 class="mb-3">
                  {{ index + 1 }}. {{ question.question_state }}
                </h5>
                <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="form-check mb-2">
                  <input
                    class="form-check-input"
                    type="radio"
                    :id="`q${index}-opt${optionIndex}`"
                    :name="`question-${index}`"
                    :value="option"
                    v-model="useranswers[question.id]"
                    :disabled="timeLeft <= 0"
                  />
                  <label class="form-check-label" :for="`q${index}-opt${optionIndex}`">
                    {{ option }}
                  </label>
                </div>
              </div>
              <div class="text-end">
                <button type="submit" class="btn btn-success">
                  <i class="fas fa-paper-plane me-1"></i>Submit
                </button>
              </div>
            </form>
          </div>

          <!-- Results Section -->
          <div v-else class="card p-4 shadow-lg border-0 bg-white">
            <h2 class="text-center text-primary fw-bold mb-4">
              <i class="fas fa-book me-2"></i>{{ Quiztitle }}
            </h2>
            <h4 class="mb-3 text-secondary">
              <i class="fas fa-chart-bar me-2"></i>Quiz Results
            </h4>

            <div v-for="(question, index) in questions" :key="index" class="mb-4">
              <h5 class="fw-semibold text-dark">
                {{ index + 1 }}. {{ question.question_state }}
              </h5>
              <div
                :class="{
                  'text-success': useranswers[question.id] === question.correct_answer,
                  'text-danger': useranswers[question.id] !== question.correct_answer
                }"
                class="ps-3"
              >
                <p class="mb-1"><strong>Your Answer:</strong> {{ useranswers[question.id] || 'No Answer' }}</p>
                <p><strong>Correct Answer:</strong> {{ getCorrectAnswerText(question) }}</p>
              </div>
              <hr />
            </div>

            <div class="text-center mt-4">
              <router-link :to="`/user_results`" class="btn btn-outline-info px-4 me-2">
                <i class="fas fa-eye me-2"></i>View Quiz Results
              </router-link>
              <router-link to="/user" class="btn btn-outline-primary px-4">
                <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
              </router-link>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name:'Start_Quiz',
    data(){
        return{
            username: '',
            Quiztitle: '',
            timeLeft: 0,
            timelimit: 0,
            questions: [],
            timer: null,
            useranswers: {},
            QuizSubmitted: false,
            noQuestions: false
        }
    },
    computed:{
        formatTime() {
            const minutes = Math.floor(this.timeLeft / 60);
            const seconds = this.timeLeft % 60;
            return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        },
        filteredQuizzes(){
            const subject= this.$route.params.subject;
            return this.quizzes.filter(quiz => quiz.subject === subject);
        }
    },
    methods:{
      async loadQuiz(){
        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/start_quiz/${this.$route.params.quiz_id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + localStorage.getItem('user_token')
          },
        })
        
        const data = await response.json();
        console.log("Fetched Quiz Data:", data);

        // Handle case where no questions are available
        if (data && data.questions && data.questions.length > 0) {
        this.noQuestions = false;
        this.Quiztitle = data.title;
        this.timelimit = data.time_limit;
        this.timeLeft = this.timelimit;
        this.questions = data.questions.map(question => ({
            id: question.id,
            question_state: question.question_state,
            options: [question.option_1, question.option_2, question.option_3, question.option_4]
        }));
        
        this.startCountdown(); // ADD THIS LINE HERE
        
    } else {
        this.noQuestions = true;
        console.error('No questions found for this quiz.');
    }
},
      getCorrectAnswerText(question) {
    const answerKey = question.correct_answer;
    
    
    if (question.options) {
    
      const optionIndex = parseInt(answerKey.slice(-1)) - 1;
      return question.options[optionIndex];
    }
    return 'N/A';
  },

  getAnswerText(question, userAnswerValue) {
    return userAnswerValue;
  },
      startCountdown() {
        this.timer = setInterval(() => {
          this.timeLeft--;
          if (this.timeLeft <= 0) {
            clearInterval(this.timer);
            this.QuizSubmitted = true;
            this.submitQuiz();
          }
        }, 1000);
      },
      prepareAnswers() {
          const answers = {};
          for (const questionId in this.useranswers) {
              answers[questionId] = this.useranswers[questionId];
          }
          return answers;
      },

      async submitQuiz(){
        clearInterval(this.timer);
        this.QuizSubmitted = true;
        const payload={
          answers: this.prepareAnswers(),
        };

        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/start_quiz/${this.$route.params.quiz_id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + localStorage.getItem('user_token')
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("Submission Response:", data);

        if (data && data.questions) {
            this.questions = data.questions.map(question => ({
                id: question.id,
                question_state: question.question_state,
                options: question.options,
                correct_answer: question.correct_answer
            }));
        }
        
      }
    },
    mounted(){
      this.username = localStorage.getItem('username') || 'User';
      this.loadQuiz(); // Only load the quiz here
    }
}
</script>

<style scoped>
</style>