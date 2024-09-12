<template>
    <div class="signup-container">
        <h2>Sign Up</h2>
        <form @submit.prevent="signupUser">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <div class="form-group">
                <input type="radio" id="user" value="user" v-model="role" required>
                <label for="user">User</label>
                <input type="radio" id="librarian" value="librarian" v-model="role" required>
                <label for="librarian">Librarian</label>
            </div>
            <button type="submit">Sign Up</button>
        </form>
        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            username: '',
            email: '',
            password: '',
            role: 'user',  // Default role is 'user'
            errorMessage: '',
        };
    },
    methods: {
        async signupUser() {
            try {
                await axios.post('http://127.0.0.1:5000/api/signup', {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    role: this.role
                });
                this.$router.push('/login');
            } catch (error) {
                this.errorMessage = error.response ? error.response.data.message : 'Signup Failed. Please try again.';
            }
        }
    }
}
</script>

<style scoped>
.signup-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="text"],
input[type="email"],
input[type="password"] {
    width: 100%;
    padding: 8px;
    margin: 4px 0;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #358a65;
}

.error-message {
    margin-top: 20px;
    color: red;
    text-align: center;
}
</style>
