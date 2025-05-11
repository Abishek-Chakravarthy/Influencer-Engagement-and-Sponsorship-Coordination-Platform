<template>
  <SponsorHeader></SponsorHeader>
  <div class="campaign-details">
    
    <h2>{{ campaign.name }}</h2>
    <h3>Current Ad Requests</h3>
    <div v-if="adRequests.length">
      <div v-for="adRequest in adRequests" :key="adRequest.id" class="ad-request-box">
        <h4>{{ adRequest.influencerName }}</h4>
        <p>Requirements: {{ adRequest.requirements }}</p>
        <p>Message: {{ adRequest.message }}</p>
        <p>Payment Amount: ${{ adRequest.paymentAmount }}</p>
        <p>Status: {{ adRequest.status }}</p>
        <button @click="showEditAdRequestDialogfunc(adRequest)" class="edit-btn">Edit</button>
        <button @click="deleteAdRequest(adRequest.id)" class="delete-btn">Delete</button>
      </div>
    </div>
    <p v-else>No AdRequests found</p>
    <button @click="showAddAdRequestDialog = true" class="add-ad-request-btn">Create Ad Request</button>
    <AddAdRequestDialog
      v-if="showAddAdRequestDialog"
      :campaignId="campaign.id"
      @close="showAddAdRequestDialog = false"
    />
    <EditAdRequestDialog
      v-if="showEditAdRequestDialog"
      :adRequest="selectedAdRequest"
      :visible="showEditAdRequestDialog"
      @close="showEditAdRequestDialog = false"
      @update="fetchAdRequests"
    />
  </div>
</template>


<script>
import AddAdRequestDialog from './AddAdRequestDialog.vue';
import SponsorHeader from './SponsorHeader.vue';
import EditAdRequestDialog from './EditAdRequestDialog.vue';
export default {
  components: {
    AddAdRequestDialog,
    SponsorHeader,
    EditAdRequestDialog
  },
  data() {
    return {
      campaign: {},  // Placeholder for campaign data
      adRequests: [], // Placeholder for ad request data
      showAddAdRequestDialog: false,
      showEditAdRequestDialog: false,
      selectedAdRequest: null
    };
  },
  props: {
    campaignId: {
      type: String, // Change to String if you cannot control the prop type outside
      required: true
    }
  },
  computed: {
    numericCampaignId() {
      return parseInt(this.campaignId);
    }
  },
  mounted() {
    this.fetchCampaignDetails();
    this.fetchAdRequests();
  },
  methods: {
    fetchCampaignDetails() {
      fetch(`/api/campaigns/${this.numericCampaignId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        this.campaign = data;
      });
    },
    fetchAdRequests() {
      fetch(`/api/ad-requests/${this.numericCampaignId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        this.adRequests = data.map(ad => ({
          ...ad,
          influencerName: ad.influencerName  // Assuming that the influencer's name is included in the response
        }));
      });
    },
    showEditAdRequestDialogfunc(adRequest) {
      this.selectedAdRequest = adRequest;
      this.showEditAdRequestDialog = true;
    },
    deleteAdRequest(adRequestId) {
      if (confirm('Are you sure you want to delete this ad request?')) {
        fetch(`/api/ad-requests/${adRequestId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${this.$store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to delete ad request');
          }
          this.fetchAdRequests();
        })
        .catch(error => {
          console.error('Error:', error);
          alert('There was a problem deleting the ad request.');
        });
      }
    }
  }
};
</script>

<style scoped>
.campaign-details {
  padding: 20px;
  background-image: url('@/assets/img1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
}
.campaign-details h3 {
  color:white;
}
.ad-request-box {
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  transition: background-color 0.3s;
  background-color:white;
}

.ad-request-box:hover {
  background-color: #f9f9f9;
}
.ad-request-box h4 {
  cursor: pointer;
}
.add-ad-request-btn {
  display: block;
  width: 50%;
  margin: 20px auto;
  padding: 10px 0;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}
.add-ad-request-btn:hover {
  background-color: #45a049;
}
button {
  margin: 5px;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}
.edit-btn {
  background-color: #2196F3;
  color: white;
}
.edit-btn:hover {
  background-color: #1e88e5;
}
.delete-btn {
  background-color: #f44336;
  color: white;
}
.delete-btn:hover {
  background-color: #e53935;
}
</style>
