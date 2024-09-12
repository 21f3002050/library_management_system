<template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="loginUser">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit">Login</button>
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
            password: '',
            errorMessage: '',
        };
    },
    methods: {
        async loginUser() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/api/login', {
                    username: this.username,
                    password: this.password
                });

                const { access_token, role } = response.data;
                localStorage.setItem('token', access_token);
                localStorage.setItem('role', role);

                if (role === 'librarian') {
                    this.$router.push('/librarian-dashboard');
                } else {
                    this.$router.push('/user-dashboard');
                }
            } catch (error) {
                this.errorMessage = error.response ? error.response.data.message : 'Login Failed. Please try again';
            }
        }
    }
}
</script>

<style scoped>
.login-container {
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
