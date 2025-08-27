<template>
  <div class="container py-5 d-flex justify-content-center">
    <div class="card shadow-lg p-4 w-100" style="max-width: 500px;">
      <h3 class="card-title text-center mb-4">📘 Add New Chapter</h3>
      <form @submit.prevent="addChapter">
        <div class="mb-3">
          <label for="name" class="form-label fw-semibold">Chapter Name</label>
          <input
            v-model="newChapter.name"
            type="text"
            class="form-control"
            id="name"
            placeholder="Enter chapter name"
            required
          />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label fw-semibold">Description</label>
          <textarea
            v-model="newChapter.description"
            class="form-control"
            id="description"
            placeholder="Enter chapter description"
            rows="4"
            required
          ></textarea>
        </div>

        <div class="d-grid">
          <button type="submit" class="btn btn-primary">
            ➕ Add Chapter
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newChapter: {
        name: '',
        description: ''
      }
    };
  },
  methods: {
    addChapter() {
      fetch(`https://quiz-app-v2-py9b.onrender.com/add_chapter/${this.$route.params.subject_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.newChapter),
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.$router.push(`/manage_subject`);
      });
    }
  }
}
</script>

<style scoped>
.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #0d6efd;
}

</style>
