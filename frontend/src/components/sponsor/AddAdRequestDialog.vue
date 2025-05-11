<template>
  <div class="dialog-overlay" @click.self="close">
    <div class="dialog">
      <h2>Add Ad Request</h2>
      <form @submit.prevent="submitAdRequest" class="ad-form">
        <div class="form-group">
          <label for="ad_name">Ad Name:</label>
          <input id="ad_name" v-model="adRequest.ad_name" required>
        </div>
        <div class="form-group">
          <label for="ad_desc">Ad Description:</label>
          <textarea id="ad_desc" v-model="adRequest.ad_desc" required></textarea>
        </div>
        <div class="form-group">
          <label for="ad_terms">Ad Terms:</label>
          <textarea id="ad_terms" v-model="adRequest.ad_terms" required></textarea>
        </div>
        <div class="form-group">
          <label for="requirements">Requirements:</label>
          <textarea id="requirements" v-model="adRequest.requirements" required></textarea>
        </div>
        <div class="form-group">
          <label for="payment_amount">Payment Amount:</label>
          <input id="payment_amount" type="number" v-model.number="adRequest.payment_amount" required>
        </div>
        <div class="form-group">
          <label for="niche">Niche:</label>
          <input id="niche" v-model="niche" @input="fetchInfluencers" required>
        </div>
        <div class="form-group">
          <label for="influencer">Select Influencer:</label>
          <select id="influencer" v-model="adRequest.influencer_id" required>
            <option v-for="influencer in influencers" :value="influencer.id" :key="influencer.id">
              {{ influencer.username }}
            </option>
          </select>
        </div>
        <button type="submit" class="done-btn">Done</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: ['campaignId'],
  data() {
    return {
      adRequest: {
        campaign_id: this.campaignId, 
        ad_name: '',
        ad_desc: '',
        ad_terms: '',
        requirements: '',
        payment_amount: 0,
        influencer_id: null,
        req_by:'sponsor'
      },
      niche: '',
      influencers: [],
      errorMessage: ''  // To store error messages
    };
  },
  watch: {
    campaignId(newVal) {
      this.adRequest.campaign_id = newVal; // Ensure campaign_id updates if prop changes
    }
  },
  methods: {
    fetchInfluencers() {
      fetch(`/api/influencers/by-niche?niche=${encodeURIComponent(this.niche)}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        this.influencers = data;
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },
    submitAdRequest() {
      // Ensure the campaign_id is set correctly
      this.adRequest.campaign_id = this.campaignId;

      console.log('Submitting ad request with campaign ID:', this.campaignId); // Debugging line

      fetch('/api/ad-requests', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...this.adRequest,
          status: 'pending'
        })
      })
      .then(response => response.json().then(data => ({ status: response.status, body: data })))
      .then(({ status, body }) => {
        if (status === 201) {
          alert('Ad request submitted successfully');
          this.close();
        } else {
          this.errorMessage = body.message || 'Error submitting ad request';
          alert(this.errorMessage);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        this.errorMessage = 'Error submitting ad request.';
        alert(this.errorMessage);
      });
    },
    close() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 500px;
}

.ad-form {
  display: grid;
  grid-gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input, .form-group select, .form-group textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.done-btn {
  display: block;
  width: 100%;
  margin-top: 20px;
  padding: 10px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.done-btn:hover {
  background-color: #45a049;
}
</style>
