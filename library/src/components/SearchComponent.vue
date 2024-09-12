<template>
    <div class="search-container">
      <div class="search-bar">
        <input v-model="query" placeholder="Search..." class="search-input" />
        <button @click="searchSections" class="search-button">Search</button>
      </div>
      
      <div v-if="sections.length" class="results-section">
        <h3>Sections</h3>
        <ul class="results-list">
          <li v-for="section in sections" :key="section.id" class="result-item">
            <h4>{{ section.name }}</h4>
            <p>{{ section.description }}</p>
          </li>
        </ul>
      </div>
  
      <div v-if="ebooks.length" class="results-section">
        <h3>E-books</h3>
        <ul class="results-list">
          <li v-for="ebook in ebooks" :key="ebook.id" class="result-item">
            <h4>{{ ebook.name }}</h4>
            <p>{{ ebook.author }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        query: '',
        sections: [],
        ebooks: []
      };
    },
    methods: {
      async searchSections() {
        try {
          const response = await axios.get('/api/user/sections/search', {
            params: { query: this.query }
          });
          this.sections = response.data.sections;
        } catch (error) {
          console.error('Error searching sections:', error);
        }
      },
      async searchEbooks(sectionId) {
        try {
          const response = await axios.get(`/api/user/sections/${sectionId}/ebooks/search`, {
            params: { query: this.query }
          });
          this.ebooks = response.data.ebooks;
        } catch (error) {
          console.error('Error searching e-books:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .search-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .search-bar {
    display: flex;
    margin-bottom: 20px;
  }
  
  .search-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .search-button {
    padding: 10px 20px;
    margin-left: 10px;
    background-color: #42b983;
    border: none;
    border-radius: 4px;
    color: white;
    cursor: pointer;
    font-size: 16px;
  }
  
  .search-button:hover {
    background-color: #36976b;
  }
  
  .results-section {
    margin-top: 20px;
  }
  
  .results-list {
    list-style-type: none;
    padding: 0;
  }
  
  .result-item {
    background-color: #fff;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .result-item h4 {
    margin: 0 0 5px;
    font-size: 18px;
  }
  
  .result-item p {
    margin: 0;
    color: #666;
  }
  </style>
  