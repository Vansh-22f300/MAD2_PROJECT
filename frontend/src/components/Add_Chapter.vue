<template>
  <div class="add-chapter-container">
    <form @submit.prevent="addChapter" class="p-4">
      <h3 class="mb-3">Add Chapter</h3>
      <div class="mb-3">
        <label for="name" class="form-label">Chapter Name</label>
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
        <label for="description" class="form-label">Description</label>
        <textarea
          v-model="newChapter.description"
          class="form-control"
          id="description"
          placeholder="Enter chapter description"
          required
        ></textarea>
      </div>
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-primary">Add Chapter</button>
      </div>
    </form>
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
      fetch(`http://127.0.0.1:5000/add_chapter/${this.$route.params.subject_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'authorization':'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.newChapter),
      })
      .then(response=> response.json())
      .then(data=>{
        alert(data.message);
        this.$router.push(`/manage_subject`);
        });
    }
        
  }
}
</script>

<style scoped>
.add-chapter-container {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  width: 100%;
  max-width: 400px;
}
</style>
