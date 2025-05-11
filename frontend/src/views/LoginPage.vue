<template>
  <div class="login-page">
    <div class="login-container">
      <h2>{{ (isAdmin === 'true') ? 'Admin Login' : 'User Login' }}</h2>
      <form @submit.prevent="login">
        <input type="text" v-model="username" placeholder="Username" />
        <input type="password" v-model="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <div v-if="isAdmin !== 'true'" class="register-section">
        <p>Don't have an account?</p>
        <button @click="goToRegister('influencer')" class="register-button">Influencer Register</button>
        <button @click="goToRegister('sponsor')" class="register-button">Sponsor Register</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isAdmin: {
      type: String,
      default: 'false'
    }
  },
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: this.username, password: this.password })
      });
      const data = await response.json();
      
      if (response.ok) {
        this.$store.dispatch('login', { user: data.user, token: data.access_token });
        // Check request status for sponsors
        if (data.user.role === 'sponsor' && data.user.request_status !== 'accepted') {
          alert('The admin did not give you access to the platform yet.');
        } else if (data.user.is_flagged) {
          alert('You have been flagged by the admin, you cannot access this platform.');
        } else {
          this.redirectUser(data.user.role);
        }
      } else {
        alert(data.message);
      }
    },
    goToRegister(role) {
      // Navigate to register page with role
      this.$router.push({ name: 'register', params: { role } });
    },
    redirectUser(role) {
      // Redirect users based on role after login
      const dashboardPath = role === 'admin' ? '/admin-dashboard' : role === 'sponsor' ? '/sponsor-dashboard' : '/influencer-dashboard';
      this.$router.push(dashboardPath);
    }
  }
};
</script>



<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.login-container {
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff; /* Set background color to white */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #34495e;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #218c4a;
}

.register-section {
  text-align: center;
}

.register-button {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  margin: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #2980b9;
}
</style>