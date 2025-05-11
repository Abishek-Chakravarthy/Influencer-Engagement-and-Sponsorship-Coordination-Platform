<template>
  <InfluencerHeader></InfluencerHeader>
  <div class="influencer-find">
    <div class="search-container">
      <h1>Find Campaigns</h1>
      <div class="search-bar">
        <select v-model="selectedAttribute">
          <option value="name">Campaign Name</option>
          <option value="company">Company Name</option>
          <option value="budget">Budget</option>
          <option value="industry">Company Industry</option>
        </select>
        <input v-model="searchQuery" placeholder="Enter search term...">
        <button class="view-btn" @click="fetchCampaigns">Search</button>
      </div>
    </div>
    <div class="campaigns-container">
      <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
        <h3>{{ campaign.name }}</h3>
        <p>Company: {{ campaign.company_name }}</p>
        <p>Budget: ${{ campaign.budget }}</p>
        <button @click="openCampaignDetails(campaign)" class="view-btn">View</button>
        <button @click="showRequestForm = true; selectedCampaign = campaign" class="request-btn">Request</button>
        <div v-if="showRequestForm && selectedCampaign.id === campaign.id" class="request-form">
          <label>Message to the Sponsor:</label>
          <input v-model="newRequest.messages" placeholder="Type your message">
          <label>Your Expected Payment:</label>
          <input v-model="newRequest.payment_amount" type="number" placeholder="Enter expected payment">
          <button @click="sendRequest(campaign.id)" class="done-btn">Done</button>
        </div>
      </div>
      <p v-if="campaigns.length === 0">No campaigns found.</p>
    </div>
    <CampaignDetailsDialog
      v-if="showDetails"
      :campaign="selectedCampaign"
      :visible="showDetails"
      @close="showDetails = false"
    />
  </div>
</template>


  <script>
  import InfluencerHeader from './InfluencerHeader.vue';
  import CampaignDetailsDialog from '@/components/CampaignDetailsDialog.vue';

  export default {
    components: {
      InfluencerHeader,
      CampaignDetailsDialog
    },
    data() {
      return {
        campaigns: [],
        selectedAttribute: 'name',
        searchQuery: '',
        showDetails: false,
        selectedCampaign: null,
        showRequestForm: false,
        newRequest: {
          messages: '',
          payment_amount: ''
        }
      };
    },
    mounted() {
      this.fetchCampaigns();
    },
    methods: {
      fetchCampaigns() {
        const url = `/api/campaigns/public?attribute=${this.selectedAttribute}&query=${this.searchQuery}`;
        fetch(url, {
          headers: {
            'Authorization': `Bearer ${this.$store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          this.campaigns = data;
          this.showRequestForm = false;
        });
      },
      openCampaignDetails(campaign) {
        this.selectedCampaign = campaign;
        this.showDetails = true;
      },
      sendRequest(campaignId) {
        const requestBody = {
          campaign_id: campaignId,
          messages: this.newRequest.messages,
          payment_amount: this.newRequest.payment_amount,
          status: 'pending'
        };
        fetch('/api/influencer/create-ad-request', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.$store.state.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestBody)
        })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          this.showRequestForm = false;
          this.newRequest.messages = '';
          this.newRequest.payment_amount = '';
        });
      }
    }
  };
  </script>

  <style scoped>
.influencer-find {
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 20px;
}

.search-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8); /* White background with some transparency */
}

.search-bar {
  display: flex;
}

.search-bar input, .search-bar select, .search-bar button {
  margin-left: 10px;
}

.campaigns-container {
  display: flex;
  flex-wrap: wrap;
  padding: 20px;
}

.campaign-box {
  flex: 1 1 300px; /* Adjusted for better layout */
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  background-color: #fff;
}

.view-btn, .request-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px; /* Increase the size of the buttons */
  border-radius: 4px; /* Make buttons more aesthetic */
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-top: 10px;
  margin-right: 5px; /* Spacing between the buttons */
}

.request-btn {
  background-color: #2ecc71;
}

.view-btn:hover, .request-btn:hover {
  transform: translateY(-2px); /* Add a slight lift on hover */
}

.request-form {
  margin-top: 10px;
  text-align: center; /* Center align the contents of the request form */
}

.done-btn {
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px; /* Make buttons more aesthetic */
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  display: inline-block; /* Make it inline to center align */
  margin: 10px 0; /* Additional margin for visual spacing */
}

.done-btn:hover {
  transform: translateY(-2px); /* Add a slight lift on hover */
}

.request-form label {
  display: block;
  margin-bottom: 5px;
}
</style>