<template>
  <header>
    <h1 @click="$router.push('/influencer-dashboard')">Influencer Dashboard</h1>
    <nav>
      <button @click="$router.push('/influencer-profile')">Profile</button>
      <button @click="$router.push('/influencer-find')">Find</button>
      <button @click="$router.push('/influencer-stats')">Stats</button>
      <button @click="logout">Logout</button>
    </nav>
  </header>
</template>

<script>
export default {
  methods: {
    logout() {
      // Implement logout logic here
      this.$store.dispatch('logout');
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2c3e50; /* Dark blue for header */
  padding: 1rem;
  color: white;
}
nav button {
  background-color: #3498db; /* Blue for buttons */
  color: white;
  border: none;
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
}
nav button:hover {
  background-color: #2980b9; /* Darker blue on hover */
}
</style>
