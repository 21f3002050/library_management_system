<template>
    <div class="container mt-5">
      <h1>Manage Requests</h1>
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
              <button v-if="request.status === 'pending'" @click="updateRequest(request.id, 'approved')" class="btn btn-success btn-sm">Approve</button>
              <button v-if="request.status === 'pending'" @click="updateRequest(request.id, 'rejected')" class="btn btn-danger btn-sm">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        requests: []
      };
    },
    methods: {
      async fetchRequests() {
        try {
          const response = await fetch('http://127.0.0.1:5000/api/requests', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.requests = await response.json();
        } catch (error) {
          console.error('Error fetching requests:', error);
        }
      },
      async updateRequest(requestId, status) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/requests/${requestId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ status })
          });
  
          if (response.ok) {
            this.fetchRequests();
          } else {
            alert('Error updating request.');
          }
        } catch (error) {
          console.error('Error updating request:', error);
        }
      }
    },
    mounted() {
      this.fetchRequests();
    }
  };
  </script>
  