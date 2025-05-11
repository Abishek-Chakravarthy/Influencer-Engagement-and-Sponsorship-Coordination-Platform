<template>
  <div>
    <SponsorHeader></SponsorHeader>
    <div class="search-container">
      <h1>Find Campaigns/Influencers</h1>
      <div class="search-bar">
        <select v-model="searchType">
          <option value="campaign">Campaign</option>
          <option value="influencer">Influencer</option>
        </select>
        <select v-model="selectedAttribute">
          <option v-for="option in attributeOptions[searchType]" :value="option.value" :key="option.value">{{ option.text }}</option>
        </select>
        <input v-model="searchQuery" placeholder="Enter search term...">
        <button class="view-btn" @click="fetchSearchResults">Search</button>
      </div>
    </div>
    <div class="results-container">
      <h2 v-if="campaigns.length && (!hasSearchResults || searchType === 'campaign')">Campaigns</h2>
      <div v-for="campaign in campaigns" :key="campaign.id" class="result-box">
        <h4>{{ campaign.name }}</h4>
        <p>Company: {{ campaign.company_name }}</p>
        <p>Budget: ${{ campaign.budget }}</p>
        <button @click="openCampaignDetails(campaign)" class="view-btn">View</button>
      </div>
      <p v-if="campaigns.length === 0 && (hasSearchResults && searchType === 'campaign')">No campaigns found.</p>

      <h2 v-if="influencers.length && (!hasSearchResults || searchType === 'influencer')">Influencers</h2>
      <div v-for="influencer in influencers" :key="influencer.id" class="result-box">
        <h4>{{ influencer.name }}</h4>
        <p>Category: {{ influencer.category }}</p>
        <button @click="openInfluencerDetails(influencer)" class="view-btn">View</button>
        <button @click="toggleRequestForm(influencer)" class="request-btn">Request</button>
        <div v-if="showRequestForm && selectedInfluencer && selectedInfluencer.id === influencer.id" class="request-form">
          <select v-model="selectedCampaignId">
            <option v-for="campaign in sponsorCampaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
          </select>
          <input v-model="newRequest.requirements" placeholder="Requirements to the influencer">
          <input v-model="newRequest.paymentAmount" type="number" placeholder="Payment Amount for the Ad">
          <button @click="submitAdRequest(selectedCampaignId, influencer.id)" class="done-btn">Done</button>
        </div>        
      </div>
      <p v-if="influencers.length === 0 && (hasSearchResults && searchType === 'influencer')">No influencers found.</p>
    </div>

    <!-- Campaign Details Dialog -->
    <CampaignDetailsDialog
      v-if="showCampaignDetails"
      :campaign="selectedCampaign"
      :visible="showCampaignDetails"
      @close="showCampaignDetails = false"
    />

    <!-- Influencer Details Dialog -->
    <InfluencerDetailsDialog
      v-if="showInfluencerDetails"
      :influencer="selectedInfluencer"
      :visible="showInfluencerDetails"
      @close="showInfluencerDetails = false"
    />
  </div>
</template>

<script>
import SponsorHeader from './SponsorHeader.vue';
import CampaignDetailsDialog from '@/components/CampaignDetailsDialog.vue';
import InfluencerDetailsDialog from '@/components/influencer/InfluencerDetailsDialog.vue';

export default {
  components: {
    SponsorHeader,
    CampaignDetailsDialog,
    InfluencerDetailsDialog
  },
  data() {
    return {
      campaigns: [],
      influencers: [],
      sponsorCampaigns: [], 
      selectedAttribute: 'name',
      searchQuery: '',
      showCampaignDetails: false,
      showInfluencerDetails: false,
      selectedCampaign: null,
      selectedCampaignId: null,  // To store selected campaign id
      selectedInfluencer: null,
      searchType: 'campaign', // Default to 'campaign'
      attributeOptions: {
        campaign: [
          { text: 'Campaign Name', value: 'name' },
          { text: 'Company Name', value: 'company' },
          { text: 'Industry', value: 'industry' },
          { text: 'Budget', value: 'budget' }
        ],
        influencer: [
          { text: 'Influencer Name', value: 'name' },
          { text: 'Category', value: 'category' },
          { text: 'Niche', value: 'niche' },
          { text: 'Reach', value: 'reach' }
        ]
      },
      showRequestForm: false,  // This should be declared here
      newRequest: {
        requirements: '',
        paymentAmount: ''
      },
      hasSearchResults: false // Indicates if search has been performed
    };
  },
  mounted() {
    this.fetchPublicCampaigns();
    this.fetchInfluencers();
    this.fetchSponsorCampaigns();
  },
  methods: {
    fetchPublicCampaigns() {
      fetch('/api/campaigns/public', {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      .then(response => response.json())
      .then(data => {
        this.campaigns = data;
      });
    },
    fetchInfluencers() {
      fetch('/api/influencers/public', {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      .then(response => response.json())
      .then(data => {
        this.influencers = data;
      });
    },
    fetchSponsorCampaigns() {
      fetch('/api/sponsor/campaigns', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => this.sponsorCampaigns = data);
    },
    fetchSearchResults() {
      this.campaigns = [];
      this.influencers = [];
      const apiUrl = `/api/sponsor/search?type=${this.searchType}&attribute=${this.selectedAttribute}&query=${this.searchQuery}`;
      fetch(apiUrl, {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      .then(response => response.json())
      .then(data => {
        if (this.searchType === 'campaign') {
          this.campaigns = data;
        } else {
          this.influencers = data;
        }
        this.hasSearchResults = true; // Indicate that search results are being displayed
      });
    },
    clearResults() {
      this.campaigns = [];
      this.influencers = [];
      this.hasSearchResults = false;
    },
    openCampaignDetails(campaign) {
      this.selectedCampaign = campaign;
      this.showCampaignDetails = true;
    },
    openInfluencerDetails(influencer) {
      this.selectedInfluencer = influencer;
      this.showInfluencerDetails = true;
    },
    toggleRequestForm(influencer) {
      // Toggle the request form visibility and set the selected influencer
      if (this.selectedInfluencer && this.selectedInfluencer.id === influencer.id) {
        this.showRequestForm = !this.showRequestForm; // Toggle if the same influencer is clicked again
      } else {
        this.showRequestForm = true; // Show form if different influencer or no one previously selected
        this.selectedInfluencer = influencer;
      }
    },
    submitAdRequest(campaignId, influencerId) {
      const requestBody = {
        campaign_id: campaignId,
        influencer_id: influencerId,
        requirements: this.newRequest.requirements,
        payment_amount: this.newRequest.paymentAmount
      };
      fetch('/api/sponsor/create-ad-request', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to create ad request');
        }
        return response.json();
      })
      .then(() => {
        alert('Ad request submitted successfully');
        this.showRequestForm = false;
        this.newRequest = { requirements: '', paymentAmount: '' };
        this.selectedInfluencer = null; // Clear the selected influencer
        this.selectedCampaignId=null;
        this.selectedCampaign = null;
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error submitting ad request.');
      });
    }
  }
};
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f4f4f4;
}

.search-bar {
  display: flex;
}

.search-bar select, .search-bar input, .search-bar button {
  margin-left: 10px;
}

.results-container {
  padding: 20px;
  background-image: url('@/assets/img1.png'); /* Add this line */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh; /* Ensure the background covers the entire height */
}

.results-container h2, h3 {
  color: white;
}

.result-box {
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

.view-btn, .request-btn {
  margin-top: 10px;
  margin-right: 5px; /* Spacing between the buttons */
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px; /* Increase the size of the buttons */
  border-radius: 4px; /* Make buttons more aesthetic */
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.request-btn {
  background-color: #2ecc71;
}

.view-btn:hover, .request-btn:hover {
  transform: translateY(-2px); /* Add a slight lift on hover */
}

.request-form {
  display: block;
  margin-top: 10px;
}

.request-form select, .request-form input, .request-form button {
  margin-top: 10px;
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.done-btn {
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  background-color: #27ae60;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.done-btn:hover {
  transform: translateY(-2px); /* Add a slight lift on hover */
}
</style>