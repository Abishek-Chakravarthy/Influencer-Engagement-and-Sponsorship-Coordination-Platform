<template>
  <header class="admin-header">
    <h1 @click="navigate('admin-dashboard')" class="clickable">Admin's Dashboard</h1>
    <nav>
      <button @click="navigate('sponsor-requests')">Sponsor Requests</button>
      <button @click="navigate('find')">Find</button>
      <button @click="navigate('stats')">Stats</button>
      <button @click="logout">Logout</button>
    </nav>
  </header>
</template>

<script>
export default {
  methods: {
     navigate(section) {
      if (section === 'admin-dashboard') {
        this.$router.push('/admin-dashboard');
      } else if (section === 'sponsor-requests') {
        this.$router.push('/sponsor-requests');
      } else if (section === 'find') {
        this.$router.push('/admin-find');
      } else if (section === 'stats') {
        this.$router.push('/admin-stats');
      }
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background-color: #f4f4f4;
}
.admin-header h1 {
  cursor: pointer; /* Change cursor to pointer to indicate clickable */
}
.admin-header nav button {
  margin-left: 10px;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.admin-header nav button:hover {
  background-color: #2980b9;
}
</style>
