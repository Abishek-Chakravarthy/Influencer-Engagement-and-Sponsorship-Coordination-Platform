<template>
  <div class="admin-find">
    <AdminHeader></AdminHeader>
    <section class="find-section">
      <h2>Find Users/Campaigns</h2>
      <div class="search-controls">
        <select v-model="selectedOption" @change="updateOptions">
          <option value="campaign">Campaign</option>
          <option value="sponsor">Sponsor</option>
          <option value="influencer">Influencer</option>
        </select>
        <select v-model="selectedAttribute">
          <option v-for="option in options" :key="option" :value="option">{{ option }}</option>
        </select>
        <input type="text" v-model="searchQuery" placeholder="Enter search query" />
        <button class="view-btn" @click="search">Search</button>
      </div>
    </section>
    <section class="results-section">
      <div class="users">
        <h4>Users</h4>
        <div v-if="users.length" class="users-list">
          <div v-for="user in users" :key="user.id" class="user-box">
            <h3>{{ user.role }}</h3>
            <p>Username: {{ user.name }}</p>
            <button class="view-btn" @click="viewUser(user)">View</button>
            <button class="flag-btn" @click="flagUser(user.id)">Flag</button>
          </div>
        </div>
        <p v-else>No users found.</p>
      </div>
      <div class="campaigns">
        <h4>Campaigns</h4>
        <div v-if="campaigns.length" class="campaigns-list">
          <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
            <p><strong>Campaign</strong>: {{ campaign.name }}</p>
            <button class="view-btn" @click="viewCampaign(campaign)">View</button>
            <button class="flag-btn" @click="flagCampaign(campaign.id)">Flag</button>
          </div>
        </div>
        <p v-else>No campaigns found.</p>
      </div>
    </section>
    <AdminViewDialog
      v-if="showAdminViewDialog"
      :type="selectedType"
      :data="selectedData"
      @close="showAdminViewDialog = false"
    />
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
      selectedOption: 'campaign',
      selectedAttribute: '',
      searchQuery: '',
      options: [],
      users: [],
      campaigns: [],
      showAdminViewDialog: false,
      selectedType: '',
      selectedData: null
    };
  },
  mounted() {
    this.updateOptions();
    this.loadAllData();
  },
  methods: {
    updateOptions() {
      if (this.selectedOption === 'campaign') {
        this.options = [
          'Campaign name',
          'Campaign Company',
          'Campaign budget',
          'Campaign start date',
          'Campaign end date',
          'Campaign visibility'
        ];
      } else if (this.selectedOption === 'sponsor') {
        this.options = [
          'Sponsor name',
          'Sponsor company',
          'Sponsor industry',
          'Sponsor net worth'
        ];
      } else if (this.selectedOption === 'influencer') {
        this.options = [
          'Influencer name',
          'Influencer category',
          'Influencer niche',
          'Influencer reach',
          'Influencer earnings'
        ];
      }
    },
    loadAllData() {
      fetch('/api/admin/all', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        this.users = data.users;
        this.campaigns = data.campaigns;
      });
    },
    search() {
      const url = `/api/admin/find?type=${this.selectedOption}&attribute=${this.selectedAttribute}&query=${this.searchQuery}`;
      fetch(url, {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        if (this.selectedOption === 'campaign') {
          this.campaigns = data;
          this.users = [];
        } else {
          this.users = data;
          this.campaigns = [];
        }
      });
    },
    viewUser(user) {
      this.selectedType = 'user';
      this.selectedData = user;
      this.showAdminViewDialog = true;
    },
    viewCampaign(campaign) {
      this.selectedType = 'campaign';
      this.selectedData = campaign;
      this.showAdminViewDialog = true;
    },
    flagUser(id) {
      fetch(`/api/admin/flag/user/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.ok) {
          alert('Flagged successfully');
          this.loadAllData();  // Refresh the data after flagging
        } else {
          alert('Failed to flag user.');
        }
      });
    },
    flagCampaign(id) {
      fetch(`/api/admin/flag/campaign/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.ok) {
          alert('Flagged successfully');
          this.loadAllData();  // Refresh the data after flagging
        } else {
          alert('Failed to flag campaign.');
        }
      });
    }
  }
};
</script>

<style scoped>
.admin-find {
  padding: 20px;
  height: 150vh;
  background-image: url('@/assets/img1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.find-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.find-section h2 {
  color: white;
}
.search-controls {
  display: flex;
  align-items: center;
}
.search-controls select, .search-controls input {
  margin-right: 10px;
  padding: 5px;
}
.results-section {
  margin-top: 20px;
}
.users-list, .campaigns-list {
  display: flex;
  flex-wrap: wrap;
}
.users h4,
.campaigns h4 {
  color: white;
}
.user-box, .campaign-box {
  padding: 0.5rem;
  border: 1px solid #eee;
  background-color: #f8f9fa;
  border-radius: 5px;
  margin-bottom: 10px;
  display: inline-block;
  width: calc(25% - 10px);
  margin-right: 10px;
  box-sizing: border-box;
}
button.view-btn, button.flag-btn {
  padding: 10px 16px; /* Increase padding for a larger button */
  font-size: 15px; /* Increase font size */
  border-radius: 6px; /* Slightly more rounded corners */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Smooth transitions */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add subtle shadow */
}

button.view-btn {
  background-color: #3498db; /* Blue color */
  color: white;
  border: none;
  margin-right: 10px; /* Add spacing between buttons */
}

button.view-btn:hover {
  background-color: #2980b9; /* Darker blue on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
}

button.flag-btn {
  background-color: #e74c3c; /* Red color */
  color: white;
  border: none;
}

button.flag-btn:hover {
  background-color: #c0392b; /* Darker red on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
}

</style>
