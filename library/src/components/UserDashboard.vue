
   <template>
    <div class="container mt-5">
      <h1>User Dashboard</h1>
      <button @click="logout" class="btn btn-danger mb-3">Logout</button>
      <router-link to="/search">
        <button class="btn btn-primary search-button">Search</button>
      </router-link>
  
      <div class="mb-3">
        <h2>Sections</h2>
        <div v-if="sections.length">
          <ul class="list-group">
            <li v-for="section in sections" :key="section.id" class="list-group-item">
              <h5>{{ section.name }}</h5>
              <p>{{ section.description }}</p>
              <p><small>Date Created: {{ new Date(section.date_created).toLocaleDateString() }}</small></p>
              <button @click="toggleEbooks(section.id)" class="btn btn-info btn-sm">View E-books</button>
  
              <div v-if="visibleSectionId === section.id">
                <ul class="list-group mt-3">
                  <li v-for="ebook in section.ebooks" :key="ebook.id" class="list-group-item">
                    <h5>{{ ebook.name }}</h5>
                    <p>Author: {{ ebook.author }}</p>
                    <p>{{ ebook.content }}</p>
                    <button v-if="!isEbookRequested(ebook.id)" @click="requestEbook(ebook.id)" class="btn btn-primary btn-sm">Request E-book</button>
                    <button v-if="isEbookRequested(ebook.id) && isEbookApproved(ebook.id)" @click="returnEbook(ebook.id)" class="btn btn-warning btn-sm">Return E-book</button>
                  </li>
                </ul>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No sections available.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sections: [],
        visibleSectionId: null,
        userRequests: []
      };
    },
    methods: {
      async fetchSections() {
        try {
          const response = await fetch('http://127.0.0.1:5000/api/user/sections', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          const sections = await response.json();
          for (let section of sections) {
            const ebooksResponse = await fetch(`http://127.0.0.1:5000/api/user/sections/${section.id}/ebooks`, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              }
            });
            section.ebooks = await ebooksResponse.json().then(data => data.ebooks);
          }
          this.sections = sections;
        } catch (error) {
          console.error('Error fetching sections and e-books:', error);
        }
      },
      async fetchUserRequests() {
        try {
          const response = await fetch('http://127.0.0.1:5000/api/user/requests', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.userRequests = await response.json();
        } catch (error) {
          console.error('Error fetching user requests:', error);
        }
      },
      isEbookRequested(ebookId) {
        return this.userRequests.some(req => req.ebook_id === ebookId && req.status === 'pending');
      },
      isEbookApproved(ebookId) {
        return this.userRequests.some(req => req.ebook_id === ebookId && req.status === 'approved');
      },
      async requestEbook(ebookId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/user/ebooks/${ebookId}/request`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ ebook_id: ebookId })
          });
  
          if (response.ok) {
            alert('E-book requested successfully.');
            this.fetchUserRequests(); // Update requests after successful request
          } else {
            alert('Error requesting e-book.');
          }
        } catch (error) {
          console.error('Error requesting e-book:', error);
        }
      },
      async returnEbook(ebookId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/user/ebooks/${ebookId}/return`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
  
          if (response.ok) {
            alert('E-book returned successfully.');
            this.fetchUserRequests(); // Update requests after successful return
          } else {
            alert('Error returning e-book.');
          }
        } catch (error) {
          console.error('Error returning e-book:', error);
        }
      },
      toggleEbooks(sectionId) {
        this.visibleSectionId = this.visibleSectionId === sectionId ? null : sectionId;
      },
      logout() {
        localStorage.removeItem('token');
        this.$router.push('/login');
      }
    },
    mounted() {
      this.fetchSections();
      this.fetchUserRequests(); // Fetch user requests when component is mounted
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
  }
  
  .search-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    margin-left: 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .search-button:hover {
    background-color: #0056b3;
  }
  </style>
  