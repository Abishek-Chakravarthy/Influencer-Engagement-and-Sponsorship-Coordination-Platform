<template>
  <div class="home-page">
    <div v-if="showWelcome" class="welcome-section">
      <h1>Welcome to IESCP</h1>
      <button @click="navigateToLogin('admin')" class="login-button">Admin Login</button>
      <button @click="navigateToLogin('user')" class="login-button">User Login</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showWelcome: true,
    };
  },
  methods: {
    navigateToLogin(userType) {
      const isAdmin = userType === 'admin';
      console.log("isAdmin =",isAdmin);
      this.$router.push({ name: 'login', params: { isAdmin } });
    }
  }
};
</script>

<style scoped>
.home-page {
  text-align: center;
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh; /* Ensure the background covers the full viewport height */
  width: 100vw; /* Ensure the background covers the full viewport width */
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0; /* Remove any default margins */
  padding: 0; /* Remove any default padding */
}

.welcome-section {
  background-color: #ecf0f1;
  padding: 50px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 40px;
}

.login-button {
  background-color: #3498db;
  color: white;
  padding: 15px 30px;
  margin: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #2980b9;
}
</style>
