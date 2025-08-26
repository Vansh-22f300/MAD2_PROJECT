<template>
  <div class="bg-light min-vh-100 d-flex align-items-center justify-content-center">
    <div class="col-md-8 col-lg-6">
      <div class="card shadow-lg border-0">
        <div class="card-header bg-primary text-white text-center py-4">
          <h4 class="mb-0">
            <i class="fas fa-user-plus me-2"></i> Create an Account
          </h4>
        </div>
        <div class="card-body px-5 py-4">
          <form @submit.prevent="signup">
            <!-- Full Name -->
            <div class="mb-3">
              <label for="full_name" class="form-label">Full Name</label>
              <input type="text" v-model="full_name" id="full_name" class="form-control" placeholder="Your full name" required />
            </div>

            <!-- Email -->
            <div class="mb-3">
              <label for="email" class="form-label">Email Address</label>
              <input type="email" v-model="email" id="email" class="form-control" placeholder="name@example.com" required />
            </div>

            <!-- Username -->
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" v-model="username" id="username" class="form-control" placeholder="Choose a username" required />
            </div>

            <!-- Password -->
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" v-model="password" id="password" class="form-control" placeholder="Enter a strong password" required />
            </div>

            <!-- Date of Birth -->
            <div class="mb-3">
              <label for="dob" class="form-label">Date of Birth</label>
              <input type="date" v-model="dob" id="dob" class="form-control" required />
            </div>
            <!-- Gender -->
            <div class="mb-3">
              <label for="gender" class="form-label">Gender</label>
              <select v-model="gender" id="gender" class="form-control" required>
                <option value="" disabled>Select your gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <!-- Phone -->
            <div class="mb-3">
              <label for="phone" class="form-label">Phone Number</label>
              <input type="tel" v-model="phone" id="phone"  class="form-control" placeholder="Your phone number must be 10 digits" required />
            </div>

            <!-- Address -->
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <textarea v-model="address" id="address" class="form-control" rows="3" placeholder="Your address" required></textarea>
            </div>
            <!-- Qualification -->
            <div class="mb-4">
              <label for="qualification" class="form-label">Qualification</label>
              <input type="text" v-model="qualification" id="qualification" class="form-control" placeholder="e.g. B.Tech, M.Sc" />
            </div>
           

            <!-- Submit Button -->
            <div class="d-grid">
              <button type="submit" class="btn btn-primary btn-lg">
                <i class="fas fa-user-check me-2"></i> Sign Up
              </button>
            </div>
          </form>
        </div>
        <div class="card-footer text-center py-3">
          <small>Already have an account? <router-link to="/login">Login here</router-link></small>
        </div>
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
