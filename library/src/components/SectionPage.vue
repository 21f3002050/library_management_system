<template>
    <div class="container mt-5">
      <h1>Section: {{ section.name }}</h1>
      <p>{{ section.description }}</p>
      <p><small>Date Created: {{ new Date(section.date_created).toLocaleDateString() }}</small></p>
      <button @click="goToEbookListPage" class="btn btn-primary">Manage E-books</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        section: {}
      };
    },
    methods: {
      async fetchSection() {
        const sectionId = this.$route.params.sectionId;
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/sections/${sectionId}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          const data = await response.json();
          this.section = data;
        } catch (error) {
          console.error('Error fetching section:', error);
        }
      },
      goToEbookListPage() {
        this.$router.push({ name: 'EbookList', params: { sectionId: this.$route.params.sectionId } });
      }
    },
    mounted() {
      this.fetchSection();
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
  }
  </style>
  