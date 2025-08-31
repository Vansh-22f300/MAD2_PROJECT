<template>
  <div class="auth-container py-5">
    
    <div class="auth-card shadow-lg p-4 p-sm-5 large-form">
      <div class="text-center mb-4">
        <i class="bi bi-person-plus-fill brand-icon"></i>
        <h3 class="mt-3 fw-bold">Create an Account</h3>
        <p class="text-muted small">Join QuizMaster to start your journey</p>
      </div>

      <form @submit.prevent="signup">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="full_name" class="form-label">Full Name</label>
            <input type="text" v-model="full_name" id="full_name" class="form-control" placeholder="Your full name" required />
          </div>

          <div class="col-md-6 mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" v-model="username" id="username" class="form-control" placeholder="Choose a username" required />
          </div>

          <div class="col-md-6 mb-3">
            <label for="email" class="form-label">Email Address</label>
            <input type="email" v-model="email" id="email" class="form-control" placeholder="name@example.com" required />
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="phone" class="form-label">Phone Number</label>
            <input type="tel" v-model="phone" id="phone" class="form-control" placeholder="10-digit number" required />
          </div>

          <div class="col-md-12 mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" v-model="password" id="password" class="form-control" placeholder="Enter a strong password" required />
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="dob" class="form-label">Date of Birth</label>
            <input type="date" v-model="dob" id="dob" class="form-control" required />
          </div>

          <div class="col-md-6 mb-3">
            <label for="gender" class="form-label">Gender</label>
            <select v-model="gender" id="gender" class="form-control" required>
              <option value="" disabled>Select your gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="col-md-12 mb-3">
            <label for="address" class="form-label">Address</label>
            <textarea v-model="address" id="address" class="form-control" rows="2" placeholder="Your address" required></textarea>
          </div>

          <div class="col-md-12 mb-4">
            <label for="qualification" class="form-label">Highest Qualification</label>
            <input type="text" v-model="qualification" id="qualification" class="form-control" placeholder="e.g. B.Tech, M.Sc" />
          </div>
        </div>
        
        <div class="d-grid">
          <button type="submit" class="btn btn-primary-custom btn-lg fw-semibold">
            Create Account
          </button>
        </div>
      </form>

      <div class="text-center mt-4">
        <small class="text-muted">Already have an account? <router-link to="/login">Login here</router-link></small>
      </div>
    </div>

  </div>
</template>
<script>
export default {
  name: "Signup",
  data() {
    return {
      full_name: "",
      email: "",
      username: "",
      password: "",
      dob: "",
      gender: "",
      phone: "",
      address: "",
      qualification: "",
    };
  },
  methods: {
    async signup() {
      const response = await fetch("https://quiz-app-v2-py9b.onrender.com/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: this.full_name,
          email: this.email,
          username: this.username,
          password: this.password,
          dob: this.dob,
          gender: this.gender,
          phone: this.phone,
          address: this.address,
          qualification: this.qualification,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert("Signup successful! Please login.");
        this.$router.push("/login");
      } else {
        alert(data.message || "Signup failed. Please try again.");
      }
    },
  },
};
</script>