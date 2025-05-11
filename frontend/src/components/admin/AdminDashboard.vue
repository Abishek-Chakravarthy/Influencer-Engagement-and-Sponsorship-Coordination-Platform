<template>
  <div class="admin-dashboard">
    <section class="welcome-section">
      <AdminHeader></AdminHeader>
    </section>
    <section class="ongoing-campaigns">
      <h2>Ongoing Campaigns</h2>
      <div v-if="campaigns.length" class="campaigns-list">
        <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
          <h3>Name: {{ campaign.name }}</h3>
          <p>Company: {{ campaign.company_name }}</p>
          <p>Budget: ${{ campaign.budget }}</p>
          <button @click="openAdminViewDialog('campaign', campaign)">View</button>
        </div>
      </div>
      <p v-else>No active campaigns found.</p>
    </section>
    <AdminViewDialog
      v-if="showAdminViewDialog"
      :type="selectedType"
      :data="selectedData"
      @close="showAdminViewDialog = false"
    />
    <section class="flagged-users">
      <h2>Flagged Users/Campaigns</h2>
      <div class="flagged-list">
        <div v-if="flaggedItems.length">
          <div v-for="flagged in flaggedItems" :key="flagged.id" class="flagged-box">
            <h3 v-if="flagged.type === 'campaign'">Campaign: {{ flagged.name }}</h3>
            <h3 v-else>{{ flagged.role }}: {{ flagged.name }}</h3>
            <button @click="openAdminViewDialog(flagged.type, flagged)">View</button>
            <button @click="removeFlagged(flagged)">Remove</button>
          </div>
        </div>
        <p v-else>No flagged users or campaigns found.</p>
      </div>
    </section>
  </div>
</template>

<script>
import AdminHeader from './AdminHeader.vue';
import AdminViewDialog from './AdminViewDialog.vue';

export default {
  components: {
    AdminHeader,
    AdminViewDialog
  },
  data() {
    return {
      adminName: 'Admin',
      campaigns: [],
      flaggedItems: [],
      showAdminViewDialog: false,
      selectedType: '',
      selectedData: null
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      // Fetch ongoing campaigns from backend
      fetch('/api/admin/campaigns', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        this.campaigns = data;
      });

      // Fetch flagged users/campaigns from backend
      fetch('/api/admin/flagged', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        this.flaggedItems = data;
      });
    },
    openAdminViewDialog(type, data) {
      this.selectedType = type;
      this.selectedData = data;
      this.showAdminViewDialog = true;
    },
    removeFlagged(item) {
      const url = item.type === 'campaign' ? `/api/admin/remove-flag/campaign/${item.id}` : `/api/admin/remove-flag/user/${item.id}`;
      fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ is_flagged: 0 })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert(`Flag successfully removed from ${item.type === 'campaign' ? 'campaign' : item.role}`);
          this.fetchData();  // Refresh data
        } else {
          alert('Failed to remove flag');
        }
      })
      .catch(error => {
        console.error('Error removing flag:', error);
        alert('An error occurred while removing the flag.');
      });
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 20px;
}
.welcome-section, .ongoing-campaigns, .flagged-users {
  background-color: rgba(255, 255, 255, 0.8); /* White background with some transparency */
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 1300px;
}
.campaigns-list, .flagged-list {
  margin: 1rem;
  padding: 1rem;
  border: 1px solid #ccc;
}
.campaign-box, .flagged-box {
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
  background-color: #f8f9fa;
  border-radius: 5px;
  margin-bottom: 10px;
  display: inline-block; /* Make boxes inline */
  width: calc(33.33% - 20px); /* Adjust width to fit multiple boxes in a row */
  margin-right: 10px; /* Spacing between boxes */
  box-sizing: border-box;
}
.campaign-box:last-child, .flagged-box:last-child {
  border-bottom: none;
}
button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
