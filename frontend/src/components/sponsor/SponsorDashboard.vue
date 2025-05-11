<template>
  <SponsorHeader></SponsorHeader>
  <div class="sponsor-dashboard">
    
    <section class="active-campaigns">
      <h2>Active Campaigns</h2>
      <div v-if="campaigns.length">
        <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
          <h3>Name: {{ campaign.name }}</h3>
          <p>Budget: {{ campaign.budget }}</p>
          <p>Amount Spent: {{ campaign.amount_spent }}</p>
          <button class="view-btn" @click="viewCampaign(campaign.id)">View</button>
        </div>
      </div>
      <p v-else>No active campaigns found.</p>
    </section>
    <section class="new-requests">
      <h2>New Requests</h2>
      <div v-if="adRequests.length">
        <div v-for="request in adRequests" :key="request.id" class="request-box">
          <h3>{{ request.campaign_name }}</h3>
          <p>Influencer Name: {{ request.influencer_name }}</p>
          <button class="view-btn" @click="viewAdDetails(request.id)">View</button>
          <button class="accept-btn" @click="openAcceptDialog(request.id)">Accept</button>
          <button class="reject-btn" @click="rejectRequest(request.id)">Reject</button>
        </div>
      </div>
      <p v-else>No new requests found.</p>
    </section>
    <AdDetailsDialog
      v-if="showAdDetailsDialog"
      :adRequestId="selectedAdRequestId"
      :role="'sponsor'"
      @close="showAdDetailsDialog = false"
    />
    <AcceptAdDialog
      v-if="showAcceptDialog"
      :requestId="selectedRequestId"
      @close="showAcceptDialog = false"
    />
  </div>
</template>


<script>
import SponsorHeader from './SponsorHeader.vue';
import AcceptAdDialog from './AcceptAdDialog.vue';
import AdDetailsDialog from '@/components/AdDetailsDialog.vue';
export default {
  components:{SponsorHeader,AcceptAdDialog,AdDetailsDialog},
  data() {
    return {
      campaigns: [],
      adRequests: [],
      showAcceptDialog: false,
      showAdDetailsDialog: false,
      selectedRequestId: null,
      selectedAdRequestId: null,
    };
  },
  mounted() {
    this.fetchCampaigns();
    this.fetchAdRequests();
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    fetchCampaigns() {
      fetch('/api/sponsor/campaigns', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => this.campaigns = data);
    },
    fetchAdRequests() {
      fetch('/api/sponsor/ad-requests', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => this.adRequests = data);
    },
    viewCampaign(id) {
      this.$router.push(`/campaign-details/${id}`);
    },
    viewAdDetails(requestId) {
      this.selectedAdRequestId = requestId;
      this.showAdDetailsDialog = true;
    },
    openAcceptDialog(requestId) {
      this.selectedRequestId = requestId;
      this.showAcceptDialog = true;
    },
    rejectRequest(id) {
        fetch(`/api/sponsor/ad-request/reject/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            }
            this.fetchAdRequests();  // Refresh list after operation
        });
    },
  }
};
</script>

<style scoped>
.sponsor-dashboard {
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
.sponsor-dashboard > SponsorHeader {
  width: 100%; /* Ensure the header spans the full width */
}
.active-campaigns, .new-requests {
  background-color: rgba(255, 255, 255, 0.8); /* White background with some transparency */
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  width: 90%;
  max-width: 1200px;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2c3e50; /* Dark blue header */
  padding: 1rem;
  color: white;
}

nav {
  display: flex;
  align-items: center;
}

nav button {
  background-color: #3498db; /* Soft blue for buttons */
  color: white;
  border: none;
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

nav button:hover {
  background-color: #2980b9; /* Darker blue on hover */
}

.campaign-box, .request-box {
  border: 1px solid #ddd; /* Light grey border for boxes */
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f8f9fa; /* Very light grey background for boxes */
}

.campaign-box h3, .request-box h3 {
  color: #333; /* Dark grey text for titles */
}

button.view-btn {
  background-color: #3498db; /* Blue color for view buttons */
  color: white;
  border: none;
  padding: 12px 24px; /* Increase padding for larger buttons */
  margin-right: 10px; /* Add spacing between buttons */
  border-radius: 6px; /* Slightly more rounded corners */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Smooth transitions */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add subtle shadow */
}

button.view-btn:hover {
  background-color: #2980b9; /* Darker blue on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
}

button.accept-btn {
  background-color: #4CAF50; /* Green color for accept buttons */
  color: white;
  border: none;
  padding: 12px 24px; /* Increase padding for larger buttons */
  margin-right: 10px; /* Add spacing between buttons */
  border-radius: 6px; /* Slightly more rounded corners */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Smooth transitions */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add subtle shadow */
}

button.accept-btn:hover {
  background-color: #45a049; /* Darker green on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
}

button.reject-btn {
  background-color: #e74c3c; /* Red color for reject buttons */
  color: white;
  border: none;
  padding: 12px 24px; /* Increase padding for larger buttons */
  margin-right: 10px; /* Add spacing between buttons */
  border-radius: 6px; /* Slightly more rounded corners */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Smooth transitions */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add subtle shadow */
}

button.reject-btn:hover {
  background-color: #c0392b; /* Darker red on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
}


.no-data {
  text-align: center;
  color: #888; /* Grey text when no data is available */
  margin-top: 20px;
}
</style>