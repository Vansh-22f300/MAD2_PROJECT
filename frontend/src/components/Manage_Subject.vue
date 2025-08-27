<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <span class="navbar-text fw-bold text-white me-3">
          <i class="fas fa-user-circle me-2"></i>Welcome, {{ adminName }}
        </span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin"><i class="fas fa-home me-1"></i>Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_summary"><i class="fas fa-chart-bar me-1"></i>Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage_quiz"><i class="fas fa-clipboard-list me-1"></i>Manage Quizzes</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_user"><i class="fas fa-users-cog me-1"></i>Manage Users</router-link>
            </li>
          </ul>
          <form class="d-flex me-3">
            <div class="input-group">
              <input class="form-control" type="search" placeholder="Search..." v-model="searchQuery" />
              <button class="btn btn-light" type="button">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </form>
          <router-link to="/login" class="btn btn-outline-light"><i class="fas fa-sign-out-alt me-1"></i>Logout</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2><i class="fas fa-tasks me-2"></i>Manage Subjects and Chapters</h2>
        <button class="btn btn-primary" @click="addSubjectModal">
          <i class="fas fa-plus me-1"></i>Add New Subject
        </button>
      </div>

      <div v-if="filterSubjects.length === 0">
        <div class="alert alert-info">No subjects found.</div>
      </div>

      <div v-else>
        <div v-for="subject in filterSubjects" :key="subject.id" class="card mb-4 shadow-sm">
          <div class="card-header bg-light fw-bold d-flex justify-content-between align-items-center">
            {{ subject.name }}
            <div>
              <button class="btn btn-sm btn-warning me-2" @click="editSubjectModal(subject)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="btn btn-sm btn-danger" @click="deleteSubject(subject.id)">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <div class="card-body">
            <p class="mb-2"><strong>Description:</strong> {{ subject.description }}</p>
            <p class="mb-2"><strong>Code:</strong> {{ subject.code }}</p>
            <p class="mb-2"><strong>Credits:</strong> {{ subject.credits }}</p>

            <table class="table table-bordered table-striped">
              <thead class="table-secondary">
                <tr>
                  <th>Chapter Name</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in subject.chapters" :key="chapter.id">
                  <td>{{ chapter.name }}</td>
                  <td>{{ chapter.description }}</td>
                  <td>
                    <button class="btn btn-sm btn-outline-secondary me-2" @click="editChapterModal(chapter)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="deleteChapter(chapter.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <router-link 
              class="btn btn-sm btn-primary" 
              :to="'/add_chapter/' + subject.id"
            >
              <i class="fas fa-plus me-1"></i>Add Chapter
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Subject Modal -->
    <div class="modal fade" id="addSubjectModal" tabindex="-1" aria-labelledby="addSubjectModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="addSubjectModalLabel">Add New Subject</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSubject">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name</label>
                <input type="text" class="form-control" id="subjectName" v-model="newSubject.name" required>
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea class="form-control" id="subjectDescription" v-model="newSubject.description" required></textarea>
              </div>
              <div class="mb-3">
              <label for="subjectCode" class="form-label">Code</label>
              <input type="text" class="form-control" id="subjectCode" v-model="newSubject.code" required>
              </div>
              <div class="mb-3">
                <label for="subjectCredits" class="form-label">Credits</label>
                <input type="number" class="form-control" id="subjectCredits" v-model="newSubject.credits" required>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Add Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Edit Subject Modal -->
    <div class="modal fade" id="editSubjectModal" tabindex="-1" aria-labelledby="editSubjectModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="editSubjectModalLabel">Edit Subject</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editSubject">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name</label>
                <input type="text" class="form-control" id="subjectName" v-model="selectedSubject.name" required>
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea class="form-control" id="subjectDescription" v-model="selectedSubject.description" required></textarea>
              </div>
              <div class="mb-3">
              <label for="subjectCode" class="form-label">Code</label>
              <input type="text" class="form-control" id="subjectCode" v-model="selectedSubject.code" required>
              </div>
              <div class="mb-3">
                <label for="subjectCredits" class="form-label">Credits</label>
                <input type="number" class="form-control" id="subjectCredits" v-model="selectedSubject.credits" required>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Edit Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Edit Chapter Modal -->
    <div class="modal fade" id="editChapterModal" tabindex="-1" aria-labelledby="editChapterModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="editChapterModalLabel">Edit Chapter</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editChapter">
              <div class="mb-3">
                <label for="chapterName" class="form-label">Chapter Name</label>
                <input type="text" class="form-control" id="chapterName" v-model="selectedChapter.name" required>
              </div>
              <div class="mb-3">
                <label for="chapterDescription" class="form-label">Description</label>
                <textarea class="form-control" id="chapterDescription" v-model="selectedChapter.description" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Edit Chapter</button>
              </div>
            </form>
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
      subjects: [],
      searchQuery: '',
      newSubject: {
        name: '',
        description: '',
        code: '',
        credits: ''
      },
      selectedSubject: {
        id: '',
        name: '',
        description: '',
        code: '',
        credits: ''
      },
      selectedChapter: {
        id: '',
        name: '',
        description: ''
      },
      adminName: ''
    };
  },
  computed: {
    filterSubjects() {
      return this.subjects.filter(subject =>
        subject.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    
  },
  methods: {
    addSubjectModal() {
      const modal = new bootstrap.Modal(document.getElementById('addSubjectModal'));
      modal.show();
    },
    async addSubject() {
      try {
        const response = await fetch('https://quiz-app-v2-py9b.onrender.com/add_subject/post', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
          },
          body: JSON.stringify({
            name: this.newSubject.name,
            description: this.newSubject.description,
            code: this.newSubject.code,
            credits: this.newSubject.credits
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert('Subject added successfully!');
          this.newSubject.name = '';
          this.newSubject.description = '';
          this.newSubject.code = '';
          this.newSubject.credits = '';
          this.fetchSubjects();
          bootstrap.Modal.getInstance(document.getElementById('addSubjectModal')).hide();
        } else {
          alert('Error: ' + data.message);
        }
      } catch (error) {
        console.error('Error adding subject:', error);
        alert('Failed to add subject.');
      }
    },
    fetchSubjects() {
      fetch('https://quiz-app-v2-py9b.onrender.com/add_subject/get', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log("Fetched data:", data);
          this.subjects = data;
        })
        .catch(error => {
          console.error('Error fetching subjects:', error);
        });
    },
    editSubjectModal(subject) {
      this.selectedSubject.id = subject.id;
      this.selectedSubject.name = subject.name;
      this.selectedSubject.description = subject.description;
      this.selectedSubject.code = subject.code;
      this.selectedSubject.credits = subject.credits;

      const modal = new bootstrap.Modal(document.getElementById('editSubjectModal'));
      modal.show();
    },
    editSubject() {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_subject/${this.selectedSubject.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify({
          name: this.selectedSubject.name,
          description: this.selectedSubject.description,
          code: this.selectedSubject.code,
          credits: this.selectedSubject.credits
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          bootstrap.Modal.getInstance(document.getElementById('editSubjectModal')).hide();
          this.fetchSubjects();
        })
        .catch(error => {
          console.error('Error editing subject:', error);
          alert('Failed to edit subject.');
        });
    },
    deleteSubject(id){
      if (confirm('Are you sure you want to delete this subject?')) {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_subject/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchSubjects();
      })
      .catch(error => {
        console.error('Error deleting subject:', error);
        alert('Failed to delete subject.');
      });
    }
    },
    editChapterModal(chapter) {
      this.selectedChapter.id = chapter.id;
      this.selectedChapter.name = chapter.name;
      this.selectedChapter.description = chapter.description;
      const modal = new bootstrap.Modal(document.getElementById('editChapterModal'));
      modal.show();
    },
    editChapter() {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_chapter/${this.selectedChapter.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify({
          name: this.selectedChapter.name,
          description: this.selectedChapter.description
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          bootstrap.Modal.getInstance(document.getElementById('editChapterModal')).hide();
          this.fetchSubjects();
        })
        .catch(error => {
          console.error('Error editing chapter:', error);
          alert('Failed to edit chapter.');
        });
    },
    deleteChapter(id){
      if (confirm('Are you sure you want to delete this chapter?')) {
      fetch(`https://quiz-app-v2-py9b.onrender.com/delete_chapter/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchSubjects();
      })
      .catch(error => {
        console.error('Error deleting chapter:', error);
        alert('Failed to delete chapter.');
      });
    }
    },
    async getAdminName() {
    try {
      const res = await fetch('https://quiz-app-v2-py9b.onrender.com/admin/profile', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      });
      const data = await res.json();
      if (res.ok) {
        this.adminName = data.username;
      } else {
        console.error(data.message);
      }
    } catch (err) {
      console.error('Error:', err);
    }
  }

  },
  mounted() {
    this.fetchSubjects();
    this.getAdminName()
  }
};
</script>
<style scoped>
.card-title {
  font-weight: bold;
  font-size: 1.25rem;
}
</style>
