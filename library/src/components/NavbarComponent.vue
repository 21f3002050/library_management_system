<!-- NavbarComponent.vue -->
<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <span class="navbar-brand">{{ username }}'s Dashboard</span>
        <div class="d-flex">
          <button class="btn btn-outline-danger" @click="logout">Logout</button>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    props: ['username'],
    methods: {
      logout() {
        // Clear the authentication token from localStorage
        localStorage.removeItem('authToken');
        // Redirect to login page
        this.$router.push('/login');
      }
    }
  };
  </script>
  