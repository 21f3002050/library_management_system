<!-- 
 <template>
  <div class="container mt-5">
    <h1>Librarian Dashboard - Section Management</h1>
    <button @click="logout" class="btn btn-danger mb-3">Logout</button> 

    <div class="mb-3">
      <h2>Create New Section</h2>
      <form @submit.prevent="createSection">
        <div class="mb-3">
          <label for="name" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="name" v-model="newSection.name" required>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea class="form-control" id="description" v-model="newSection.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Create Section</button>
      </form>
    </div>

    <div>
      <h2>Existing Sections</h2>
      <ul class="list-group">
        <li v-for="section in sections" :key="section.id" class="list-group-item">
          <h5>{{ section.name }}</h5>
          <p>{{ section.description }}</p>
          <p><small>Date Created: {{ new Date(section.date_created).toLocaleDateString() }}</small></p>
          <button @click="editSection(section)" class="btn btn-warning btn-sm me-2">Edit</button>
          <button @click="deleteSection(section.id)" class="btn btn-danger btn-sm me-2">Delete</button>
          <router-link :to="{ name: 'EbookManagement', params: { sectionId: section.id } }" class="btn btn-info btn-sm me-2">Manage E-books</router-link>
        </li>
      </ul>
    </div>

    <div v-if="selectedSection">
      <h2>Edit Section</h2>
      <form @submit.prevent="updateSection">
        <div class="mb-3">
          <label for="editName" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="editName" v-model="selectedSection.name" required>
        </div>
        <div class="mb-3">
          <label for="editDescription" class="form-label">Description</label>
          <textarea class="form-control" id="editDescription" v-model="selectedSection.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Section</button>
        <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newSection: {
        name: '',
        description: ''
      },
      sections: [],
      selectedSection: null
    };
  },
  methods: {
    async fetchSections() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/sections', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.sections = data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async createSection() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/sections', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.newSection)
        });

        if (response.ok) {
          this.newSection.name = '';
          this.newSection.description = '';
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error creating section:', error);
      }
    },
    editSection(section) {
      this.selectedSection = { ...section };
    },
    async updateSection() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${this.selectedSection.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.selectedSection)
        });

        if (response.ok) {
          this.selectedSection = null;
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error updating section:', error);
      }
    },
    async deleteSection(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
    cancelEdit() {
      this.selectedSection = null;
    },
    logout() {
      localStorage.removeItem('token'); 
      this.$router.push('/login');       
    }
  },
  mounted() {
    this.fetchSections();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>

 -->




<!-------------------------------->

 <!-- <template>
  <div class="container mt-5">
    <h1>Librarian Dashboard - Section Management</h1>
    <button @click="logout" class="btn btn-danger mb-3">Logout</button> 

    <div class="mb-3">
      <h2>Create New Section</h2>
      <form @submit.prevent="createSection">
        <div class="mb-3">
          <label for="name" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="name" v-model="newSection.name" required>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea class="form-control" id="description" v-model="newSection.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Create Section</button>
      </form>
    </div>

    <div>
      <h2>Existing Sections</h2>
      <ul class="list-group">
        <li v-for="section in sections" :key="section.id" class="list-group-item">
          <h5>{{ section.name }}</h5>
          <p>{{ section.description }}</p>
          <p><small>Date Created: {{ new Date(section.date_created).toLocaleDateString() }}</small></p>
          <router-link :to="{ name: 'EbookManagement', params: { sectionId: section.id } }" class="btn btn-info btn-sm me-2">Manage E-books</router-link>
          <button @click="editSection(section)" class="btn btn-warning btn-sm me-2">Edit</button>
          <button @click="deleteSection(section.id)" class="btn btn-danger btn-sm me-2">Delete</button>
        </li>
      </ul>
    </div>

    <div v-if="selectedSection">
      <h2>Edit Section</h2>
      <form @submit.prevent="updateSection">
        <div class="mb-3">
          <label for="editName" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="editName" v-model="selectedSection.name" required>
        </div>
        <div class="mb-3">
          <label for="editDescription" class="form-label">Description</label>
          <textarea class="form-control" id="editDescription" v-model="selectedSection.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Section</button>
        <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newSection: {
        name: '',
        description: ''
      },
      sections: [],
      selectedSection: null
    };
  },
  methods: {
    async fetchSections() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/sections', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.sections = data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async createSection() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/sections', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.newSection)
        });

        if (response.ok) {
          this.newSection.name = '';
          this.newSection.description = '';
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error creating section:', error);
      }
    },
    editSection(section) {
      this.selectedSection = { ...section };
    },
    async updateSection() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${this.selectedSection.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.selectedSection)
        });

        if (response.ok) {
          this.selectedSection = null;
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error updating section:', error);
      }
    },
    async deleteSection(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
    cancelEdit() {
      this.selectedSection = null;
    },
    logout() {
      localStorage.removeItem('token'); 
      this.$router.push('/login');       
    }
  },
  mounted() {
    this.fetchSections();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style> -->


<template>
  <div class="container mt-5">
    <h1>Librarian Dashboard</h1>
    <button @click="logout" class="btn btn-danger mb-3">Logout</button> 
    <button @click="navigateToRequests" class="btn btn-primary mb-3">Manage Requests</button>
    <button @click="navigateToStatistics" class="btn btn-secondary mb-3">View Statistics</button>

    <!-- Create New Section -->
    <div class="mb-3">
      <h2>Create New Section</h2>
      <form @submit.prevent="createSection">
        <div class="mb-3">
          <label for="name" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="name" v-model="newSection.name" required>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea class="form-control" id="description" v-model="newSection.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Create Section</button>
      </form>
    </div>

    <!-- View All Issue/Return Requests
    <div class="mb-5">
      <h2>Issue/Return Requests</h2>
      <div v-if="requests.length">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>User ID</th>
              <th>E-book ID</th>
              <th>Request Date</th>
              <th>Issue Date</th>
              <th>Return Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.user_id }}</td>
              <td>{{ request.ebook_id }}</td>
              <td>{{ new Date(request.request_date).toLocaleDateString() }}</td>
              <td>{{ request.issue_date ? new Date(request.issue_date).toLocaleDateString() : 'N/A' }}</td>
              <td>{{ request.return_date ? new Date(request.return_date).toLocaleDateString() : 'N/A' }}</td>
              <td>{{ request.status }}</td>
              <td>
                <button v-if="request.status === 'pending'" @click="approveRequest(request.id)" class="btn btn-success btn-sm">Approve</button>
                <button v-if="request.status === 'pending'" @click="rejectRequest(request.id)" class="btn btn-danger btn-sm">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No requests available.</p>
      </div>
    </div> -->

    <!-- Existing Sections -->
    <div>
      <h2>Existing Sections</h2>
      <ul class="list-group">
        <li v-for="section in sections" :key="section.id" class="list-group-item">
          <h5>{{ section.name }}</h5>
          <p>{{ section.description }}</p>
          <p><small>Date Created: {{ new Date(section.date_created).toLocaleDateString() }}</small></p>
          <router-link :to="{ name: 'EbookManagement', params: { sectionId: section.id } }" class="btn btn-info btn-sm me-2">Manage E-books</router-link>
          <button @click="editSection(section)" class="btn btn-warning btn-sm me-2">Edit</button>
          <button @click="deleteSection(section.id)" class="btn btn-danger btn-sm me-2">Delete</button>
        </li>
      </ul>
    </div>

    <!-- Edit Section -->
    <div v-if="selectedSection">
      <h2>Edit Section</h2>
      <form @submit.prevent="updateSection">
        <div class="mb-3">
          <label for="editName" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="editName" v-model="selectedSection.name" required>
        </div>
        <div class="mb-3">
          <label for="editDescription" class="form-label">Description</label>
          <textarea class="form-control" id="editDescription" v-model="selectedSection.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Section</button>
        <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newSection: {
        name: '',
        description: ''
      },
      sections: [],
      selectedSection: null,
      requests: []
    };
  },
  methods: {
    async fetchSections() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/sections', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.sections = data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async fetchRequests() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/librarian/requests', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.requests = data;
      } catch (error) {
        console.error('Error fetching requests:', error);
      }
    },
    async createSection() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/sections', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.newSection)
        });

        if (response.ok) {
          this.newSection.name = '';
          this.newSection.description = '';
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error creating section:', error);
      }
    },
    async approveRequest(requestId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/librarian/requests/${requestId}/approve`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          alert('Request approved.');
          this.fetchRequests();
        } else {
          alert('Error approving request.');
        }
      } catch (error) {
        console.error('Error approving request:', error);
      }
    },
    async rejectRequest(requestId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/librarian/requests/${requestId}/reject`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          alert('Request rejected.');
          this.fetchRequests();
        } else {
          alert('Error rejecting request.');
        }
      } catch (error) {
        console.error('Error rejecting request:', error);
      }
    },
    editSection(section) {
      this.selectedSection = { ...section };
    },
    async updateSection() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${this.selectedSection.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.selectedSection)
        });

        if (response.ok) {
          this.selectedSection = null;
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error updating section:', error);
      }
    },
    async deleteSection(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/sections/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          this.fetchSections();
        }
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
    cancelEdit() {
      this.selectedSection = null;
    },
    navigateToRequests() {
      this.$router.push('/manage-requests');
    },
    navigateToStatistics() {
      this.$router.push('/manage-statistics');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchSections();
    this.fetchRequests();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
