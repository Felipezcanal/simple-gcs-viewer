<script setup>
import Main from './components/Main.vue'
import { ref, onMounted } from 'vue'

const path = ref(import.meta.env.VITE_BASE_GCS_PATH)
if (!path.value.endsWith('/')) {
  path.value += '/'
}

function updatePath(value) {
  path.value = value
}

// Login state and credentials
const isLoggedIn = ref(false)
const loginEmail = ref('')
const loginPassword = ref('')

// Check for login state in local storage on component mount
onMounted(() => {
  const savedLoginState = localStorage.getItem('isLoggedIn')
  isLoggedIn.value = savedLoginState === 'true'
  if (isLoggedIn.value) {
    // Optionally, you might want to also store and retrieve the user's email
    loginEmail.value = localStorage.getItem('loginEmail') || ''
  }
})

async function login() {
  try {
    const response = await fetch(import.meta.env.VITE_API_URL + '/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: loginEmail.value,
        password: loginPassword.value
      })
    });

    if (response.ok) {
      isLoggedIn.value = true;
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('loginEmail', loginEmail.value)
    } else {
      const error = await response.json();
      console.error(error.detail);
      alert('Invalid credentials!');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred during login');
  }
}

</script>

<template>
  <div v-if="!isLoggedIn">
    <h2>Login</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="input-group">
        <input type="email" id="email" v-model="loginEmail" placeholder="Email" required />
      </div>
      <div class="input-group">
        <input type="password" id="password" v-model="loginPassword" placeholder="Password" required />
      </div>
      <button type="submit" class="login-button">Login</button>
    </form>
  </div>
  <div v-else>
    <Main :path="path" :updatePath="updatePath"/>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

.login-form {
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background: white;
  min-width: 300px;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
}

input[type='email'], input[type='password'] {
  width: calc(100% - 22px); /* Adjust width for padding */
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #0056b3;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #003d82;
}

h2 {
  text-align: center;
  color: #e1e1e1;
}

::placeholder {
  color: #e1e1e1;
  opacity: 1; /* Firefox */
}

::-ms-input-placeholder { /* Edge 12 -18 */
  color: #e1e1e1;
}
</style>
