<template>
    <div class="container-fluid homepage">
      <div class="row justify-content-center align-items-center vh-100">
        <div class="col-md-6 text-center">
          <h1 class="mb-4">Welcome to Your Library App</h1>
          <router-link to="/signup" class="btn custom-btn mx-2">Sign Up</router-link>
          <router-link to="/login" class="btn custom-btn mx-2">Log In</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
  };
  </script>
  
  <style scoped>
  .homepage {
    background-color: #f8f9fa; 
  }
  
  .custom-btn {
    background-color: #42b983;
    border-color: #42b983;
    color: white;
    font-size: 1.2rem;
    padding: 10px 20px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }
  
  .custom-btn:hover {
    background-color: #36a372;
    border-color: #36a372;
  }
  
  .vh-100 {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  </style>
   