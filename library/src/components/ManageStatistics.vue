<template>
    <div class="container mt-5">
      <h1>Statistics</h1>
      <ul>
        <li>Total Requests: {{ statistics.total_requests }}</li>
        <li>Total E-books: {{ statistics.total_ebooks }}</li>
        <li>Total Sections: {{ statistics.total_sections }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        statistics: {}
      };
    },
    methods: {
      async fetchStatistics() {
        try {
          const response = await fetch('http://127.0.0.1:5000/api/statistics', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.statistics = await response.json();
        } catch (error) {
          console.error('Error fetching statistics:', error);
        }
      }
    },
    mounted() {
      this.fetchStatistics();
    }
  };
  </script>
  