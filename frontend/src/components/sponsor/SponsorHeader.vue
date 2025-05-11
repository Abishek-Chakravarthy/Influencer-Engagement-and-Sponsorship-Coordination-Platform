<template>
  <header>
    <h1 @click="$router.push('/sponsor-dashboard')">Sponsor Dashboard</h1>
    <nav>
      <button @click="$router.push('/sponsor-profile')">Profile</button>
      <button @click="$router.push('/sponsor-campaigns')">Campaigns</button>
      <button @click="$router.push('/sponsor-find')">Find</button>
      <button @click="$router.push('/sponsor-stats')">Stats</button>
      <button @click="exportReport">Export Report</button>
      <button @click="logout">Logout</button>
    </nav>
  </header>
</template>

<script>
export default {
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    async exportReport() {
      try {
        const response = await fetch('/api/sponsor/export-report', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sponsor_report.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error exporting report:', error);
      }
    }
  }
}
</script>

<style scoped>
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2c3e50;
  padding: 1rem;
  color: white;
}
nav button {
  margin-left: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}
nav button:hover {
  background-color: #2980b9;
}
</style>
