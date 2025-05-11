<template>
  <InfluencerHeader></InfluencerHeader>
  <div class="influencer-dashboard">
    <section class="active-campaigns">
      <h2>Active Campaigns</h2>
      <div class="campaigns-container">
        <div v-if="campaigns.length">
          <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
            <h3>{{ campaign.campaign_name }}</h3>
            <p>Company: {{ campaign.company_name }}</p>
            <button @click="openCampaignDisplay(campaign)" class="view-btn">View</button>
          </div>
        </div>
        <p v-else>No active campaigns found.</p>
      </div>
    </section>
    <InfluencerAdDisplayDialog
      v-if="showCampaignDialog"
      :campaign="selectedCampaign"
      @close="showCampaignDialog = false"
    />
    <AdDetailsDialog
      v-if="showAdDetailsDialog"
      :adRequestId="selectedAdRequest.id"
      :role="role"
      @close="showAdDetailsDialog = false"
    />
    <section class="new-requests">
      <h2>New Requests</h2>
      <div class="requests-container">
        <div v-if="adRequests.length">
          <div v-for="request in adRequests" :key="request.id" class="request-box">
            <h3>Campaign: {{ request.campaign_name }}</h3>
            <p>Company Name: {{ request.company_name }}</p>
            <button @click="viewAdDetails(request)" class="view-btn">View</button>
            <button @click="acceptRequest(request.id)" class="accept-btn">Accept</button>
            <button @click="rejectRequest(request.id)" class="reject-btn">Reject</button>
          </div>
        </div>
        <p v-else>No new Requests found.</p>
      </div>
    </section>
  </div>
</template>


<script>
import InfluencerHeader from './InfluencerHeader.vue';
import InfluencerAdDisplayDialog from './InfluencerAdDisplayDialog.vue';
import AdDetailsDialog from '@/components/AdDetailsDialog.vue';

export default {
  components: {InfluencerHeader,InfluencerAdDisplayDialog,AdDetailsDialog},
  data() {
    return {
      campaigns: [],
      adRequests: [],
      showCampaignDialog: false,
      showAdDetailsDialog: false,
      selectedCampaign: null,
      selectedAdRequest: null,
      role: 'influencer' // Assuming the role is influencer
    };
  },
  mounted() {
    this.fetchCampaigns();
    this.fetchAdRequests();
  },
  methods: {
    logout() {
      // Implement logout functionality
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    fetchCampaigns() {
        fetch('/api/influencer/campaigns', {
            headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        })
        .then(response => response.json())
        .then(data => {
            this.campaigns = data;
            console.log("Fetched campaigns:", this.campaigns);
        })
        .catch(error => console.error('Error fetching campaigns:', error));
    },
    fetchAdRequests() {
        fetch('/api/influencer/ad-requests', {
            headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        })
        .then(response => response.json())
        .then(data => {
            this.adRequests = data.map(req => ({
                ...req,
                view: () => this.viewRequest(req.id),
                accept: () => this.acceptRequest(req.id),
                reject: () => this.rejectRequest(req.id)
            }));
        });
    },
    openCampaignDisplay(campaign) {
      console.log("Opening campaign display for:", campaign);
      this.selectedCampaign = campaign;
      this.showCampaignDialog = true;
    },
    viewAdDetails(request) {
      this.selectedAdRequest = request;
      this.showAdDetailsDialog = true;
    },
    viewRequest(request) {
      // Open AdDetailsDialog with the request details
      this.viewAdDetails(request);
    },
    acceptRequest(id) {
        fetch(`/api/influencer/ad-request/accept/${id}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        }).then(() => this.fetchAdRequests());
    },
    rejectRequest(id) {
        fetch(`/api/influencer/ad-request/reject/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        }).then(() => this.fetchAdRequests());
    },
    updateRequestStatus(id, status) {
      // Update the status of an ad request
      fetch(`/api/ad-request/update/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
      })
      .then(response => {
        if (response.ok) {
          this.fetchAdRequests();  // Refresh ad requests list after updating
        }
      });
    }
  }
};
</script>

<style scoped>
.influencer-dashboard {
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 20px;
}

.influencer-dashboard header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2c3e50;
  padding: 1rem;
  color: white;
}

.influencer-dashboard nav button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.influencer-dashboard nav button:hover {
  background-color: #2980b9;
}

section {
  background-color: rgba(255, 255, 255, 0.8); /* White background with some transparency */
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  width: 90%;
  max-width: 1200px;
  margin: 20px auto;
}

.campaigns-container, .requests-container {
  
  flex-wrap: wrap;
  justify-content: space-between; /* Spread out the boxes */
}

.campaign-box, .request-box {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  padding: 15px;
  margin: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  box-sizing: border-box;
}

.campaign-box h3, .request-box h3 {
  margin-top: 0;
  cursor: pointer;
}

.campaign-box p, .request-box p {
  margin: 5px 0;
}

button {
  margin: 5px;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 4px;
}

button:hover {
  background-color: #ddd;
}

.view-btn {
  background-color: #3498db;
  color: white;
}

.view-btn:hover {
  background-color: #2980b9;
}

.accept-btn {
  background-color: #4CAF50;
  color: white;
}

.accept-btn:hover {
  background-color: #45a049;
}

.reject-btn {
  background-color: #f44336;
  color: white;
}

.reject-btn:hover {
  background-color: #e53935;
}

.no-data {
  text-align: center;
  color: #888;
  margin-top: 20px;
}

h2 {
  text-align: center; /* Center align the headers */

}
</style>
