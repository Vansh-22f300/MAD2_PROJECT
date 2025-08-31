<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">User Dashboard</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/user" class="nav-link"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/user_results" class="nav-link"><i class="fas fa-chart-bar me-2"></i>My Results</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <div v-if="!QuizSubmitted">
        <header class="content-header">
          <div>
            <h2 class="fw-bold">{{ Quiztitle }}</h2>
            <p class="text-muted">Read each question carefully. Good luck!</p>
          </div>
        </header>
        
        <div class="quiz-layout-grid mt-4">
          <div class="questions-panel">
            <div class="data-card">
              <form @submit.prevent="submitQuiz">
                <div v-for="(question, index) in questions" :key="index" class="question-block">
                  <h5 class="question-title">
                    <span class="question-number">{{ index + 1 }}</span>
                    {{ question.question_state }}
                  </h5>
                  <div class="options-group">
                    <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="form-check">
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
                </div>
              </form>
            </div>
          </div>

          <div class="quiz-info-panel">
            <div class="data-card sticky-top" style="top: 2rem;">
              <h5 class="fw-bold text-center">Quiz Status</h5>
              <hr>
              <div class="timer-display">
                <i class="fas fa-clock me-2"></i>
                <span>Time Left:</span>
                <strong class="time-value">{{ formatTime }}</strong>
              </div>
              <div class="progress my-4" style="height: 10px;">
                <div class="progress-bar" role="progressbar" :style="{ width: progressPercentage + '%' }"></div>
              </div>
              <p class="text-center text-muted small">{{ answeredQuestions }} of {{ questions.length }} questions answered</p>
              <div class="d-grid">
                <button type="button" @click="submitQuiz" class="btn btn-success-custom btn-lg">
                  <i class="fas fa-paper-plane me-2"></i>Submit Quiz
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
  <header class="content-header text-center">
    <div>
      <h2 class="fw-bold">Quiz Completed!</h2>
      <p class="text-muted">Here's a summary of your results for "{{ Quiztitle }}"</p>
    </div>
  </header>
  <div class="results-summary-card mt-4">
      <div v-for="(question, index) in questions" :key="index" class="result-item">
          <div class="result-question">
              <strong>{{ index + 1 }}.</strong> {{ question.question_state }}
          </div>
          
          <div class="result-answer">
              <span>Your Answer: {{ useranswers[question.id] || 'No Answer' }}</span>
          </div>
          
          <div class="result-correct-answer">
              <strong>Correct Answer:</strong> {{ getCorrectAnswerText(question) }}
          </div>
      </div>
       <div class="text-center mt-4">
          <router-link to="/user_results" class="btn btn-primary-custom px-4 me-2">
              <i class="fas fa-eye me-2"></i>View All Results
          </router-link>
          <router-link to="/user" class="btn btn-outline-secondary px-4">
              <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
          </router-link>
      </div>
  </div>
</div>
    </main>
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
        },
        progressPercentage() {
            if (!this.questions.length) return 0;
            return (this.answeredQuestions / this.questions.length) * 100;
        },
        answeredQuestions() {
            return Object.keys(this.useranswers).length;
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