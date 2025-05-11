<template>
  <SponsorHeader></SponsorHeader>
  <div class="sponsor-campaigns">
    <h2>My Campaigns</h2>
    <div v-if="campaigns.length">
      <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-box">
        <h3 @click="goToCampaignDetails(campaign.id)">{{ campaign.name }}</h3>
        <p>{{ campaign.description }}</p>
        <p>End Date: {{ campaign.end_date }}</p>
        <p>Budget: ${{ campaign.budget }}</p>
        <button @click.stop="showCampaignDetails(campaign)" class="view-btn">View</button>
        <button @click.stop="showUpdateCampaign(campaign)" class="edit-btn">Edit</button>
        <button @click.stop="deleteCampaign(campaign.id)" class="delete-btn">Delete</button>
      </div>
    </div>
    <p v-else class="no-campaigns">No current campaigns found</p>
    <button @click="showAddCampaignDialog = true" class="add-campaign-btn">Add Campaign</button>
    <AddCampaignDialog
      v-if="showAddCampaignDialog"
      @close="showAddCampaignDialog = false"
    />
    <CampaignDetailsDialog
      v-if="showCampaignDetailsDialog"
      :campaign="selectedCampaign"
      :visible="showCampaignDetailsDialog"
      @close="showCampaignDetailsDialog = false"
    />
    <UpdateCampaignDialog
      v-if="showUpdateCampaignDialog"
      :campaign="selectedCampaign"
      :visible="showUpdateCampaignDialog"
      @close="showUpdateCampaignDialog = false"
      @update="fetchCampaigns"
    />
  </div>
</template>

<script>
import SponsorHeader from './SponsorHeader.vue';
import AddCampaignDialog from './AddCampaignDialog.vue';
import CampaignDetailsDialog from '@/components/CampaignDetailsDialog.vue';
import UpdateCampaignDialog from './UpdateCampaignDialog.vue';

export default {
  components: {
    SponsorHeader,
    AddCampaignDialog,
    CampaignDetailsDialog,
    UpdateCampaignDialog
  },
  data() {
    return {
      campaigns: [],
      showAddCampaignDialog: false,
      showCampaignDetailsDialog: false,
      showUpdateCampaignDialog: false,
      selectedCampaign: null
    };
  },
  mounted() {
    this.fetchCampaigns();
  },
  methods: {
    fetchCampaigns() {
      fetch('/api/sponsor/campaigns', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch campaigns');
        }
        return response.json();
      })
      .then(data => {
        this.campaigns = data;
      })
      .catch(error => {
        console.error('Error:', error);
        alert('There was a problem fetching the campaigns.');
      });
    },
    showCampaignDetails(campaign) {
      this.selectedCampaign = campaign;
      this.showCampaignDetailsDialog = true;
    },
    showUpdateCampaign(campaign) {
      this.selectedCampaign = campaign;
      this.showUpdateCampaignDialog = true;
    },
    deleteCampaign(campaignId) {
      if (confirm('Are you sure you want to delete this campaign?')) {
        fetch(`/api/campaigns/${campaignId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${this.$store.state.token}`,
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to delete campaign');
          }
          this.fetchCampaigns();
        })
        .catch(error => {
          console.error('Error:', error);
          alert('There was a problem deleting the campaign.');
        });
      }
    },
    goToCampaignDetails(campaignId) {
      this.$router.push({ name: 'campaign-details', params: { campaignId } });
    }
  }
};
</script>

<style scoped>
.sponsor-campaigns {
  background-image: url('@/assets/img1.png'); /* Add this line */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 20px;
}
.sponsor-campaigns h2 {
  color:white;
}
.campaign-box {
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  transition: background-color 0.3s;
  background-color:white;
}
.campaign-box:hover {
  background-color: #f9f9f9;
}
.campaign-box h3 {
  cursor: pointer;
}
.no-campaigns {
  text-align: center;
  margin-top: 20px;
}
.add-campaign-btn {
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
.add-campaign-btn:hover {
  background-color: #45a049;
}
button {
  margin: 5px;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}
.view-btn {
  background-color: #4CAF50;
  color: white;
}
.view-btn:hover {
  background-color: #45a049;
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
