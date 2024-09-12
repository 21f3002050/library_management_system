<template>
  <div class="container mt-5">
    <h1>E-book Management for Section: {{ section.name }}</h1>
    <button @click="logout" class="btn btn-danger mb-3">Logout</button>

    <div class="mb-3">
      <h2>Create New E-book</h2>
      <form @submit.prevent="createEbook">
        <div class="mb-3">
          <label for="name" class="form-label">E-book Name</label>
          <input type="text" class="form-control" id="name" v-model="newEbook.name" required>
        </div>
        <div class="mb-3">
          <label for="author" class="form-label">Author</label>
          <input type="text" class="form-control" id="author" v-model="newEbook.author" required>
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Content</label>
          <textarea class="form-control" id="content" v-model="newEbook.content" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Create E-book</button>
      </form>
    </div>

    <div>
      <h2>Existing E-books</h2>
      <ul class="list-group">
        <li v-for="ebook in ebooks" :key="ebook.id" class="list-group-item">
          <h5>{{ ebook.name }}</h5>
          <p>{{ ebook.author }}</p>
          <p>{{ ebook.content }}</p>
          <button @click="editEbook(ebook)" class="btn btn-warning btn-sm me-2">Edit</button>
          <button @click="deleteEbook(ebook.id)" class="btn btn-danger btn-sm me-2">Delete</button>
        </li>
      </ul>
    </div>

    <div v-if="selectedEbook">
      <h2>Edit E-book</h2>
      <form @submit.prevent="updateEbook">
        <div class="mb-3">
          <label for="editName" class="form-label">E-book Name</label>
          <input type="text" class="form-control" id="editName" v-model="selectedEbook.name" required>
        </div>
        <div class="mb-3">
          <label for="editAuthor" class="form-label">Author</label>
          <input type="text" class="form-control" id="editAuthor" v-model="selectedEbook.author" required>
        </div>
        <div class="mb-3">
          <label for="editContent" class="form-label">Content</label>
          <textarea class="form-control" id="editContent" v-model="selectedEbook.content" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update E-book</button>
        <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      section: {},
      newEbook: {
        name: '',
        author: '',
        content: ''
      },
      ebooks: [],
      selectedEbook: null
    };
  },
  methods: {
    async fetchSectionAndEbooks() {
      try {
        const sectionId = this.$route.params.sectionId;
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${sectionId}/ebooks`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.section = { name: data.section_name };
        this.ebooks = data.ebooks;
      } catch (error) {
        console.error('Error fetching section and ebooks:', error);
      }
    },
    async createEbook() {
      try {
        const sectionId = this.$route.params.sectionId;
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${sectionId}/ebooks`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.newEbook)
        });

        if (response.ok) {
          this.newEbook.name = '';
          this.newEbook.author = '';
          this.newEbook.content = '';
          this.fetchSectionAndEbooks();
        }
      } catch (error) {
        console.error('Error creating e-book:', error);
      }
    },
    editEbook(ebook) {
      this.selectedEbook = { ...ebook };
    },
    async updateEbook() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/ebooks/${this.selectedEbook.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.selectedEbook)
        });

        if (response.ok) {
          this.selectedEbook = null;
          this.fetchSectionAndEbooks();
        }
      } catch (error) {
        console.error('Error updating e-book:', error);
      }
    },
    async deleteEbook(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/ebooks/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          this.fetchSectionAndEbooks();
        }
      } catch (error) {
        console.error('Error deleting e-book:', error);
      }
    },
    cancelEdit() {
      this.selectedEbook = null;
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchSectionAndEbooks();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
