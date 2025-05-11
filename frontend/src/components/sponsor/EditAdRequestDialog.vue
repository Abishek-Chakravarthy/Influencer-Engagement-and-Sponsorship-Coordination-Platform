<template>
  <div v-if="visible" class="dialog-overlay" @click.self="close">
    <div class="dialog" role="dialog" aria-labelledby="dialogTitle">
      <h2 id="dialogTitle">Edit Ad Request</h2>
      <form @submit.prevent="updateAdRequest" class="ad-form">
        <div v-if="adRequest.status === 'pending' || adRequest.status === 'negotiated'">
          <div class="form-group">
            <label for="influencer_name">Influencer Name:</label>
            <select v-model="updatedAdRequest.influencer_id" id="influencer_name" required>
              <option v-for="influencer in influencers" :value="influencer.id" :key="influencer.id">
                {{ influencer.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="payment_amount">Payment Amount:</label>
            <input type="number" v-model="updatedAdRequest.payment_amount" id="payment_amount" required>
          </div>

          <div class="form-group">
            <label for="ad_name">Ad Name:</label>
            <input type="text" v-model="updatedAdRequest.ad_name" id="ad_name" required>
          </div>

          <div class="form-group">
            <label for="ad_desc">Ad Description:</label>
            <textarea v-model="updatedAdRequest.ad_desc" id="ad_desc"></textarea>
          </div>

          <div class="form-group">
            <label for="ad_terms">Ad Terms:</label>
            <textarea v-model="updatedAdRequest.ad_terms" id="ad_terms"></textarea>
          </div>
        </div>

        <div class="form-group">
          <label for="requirements">Requirements:</label>
          <textarea v-model="updatedAdRequest.requirements" id="requirements"></textarea>
        </div>

        <div class="form-group">
          <label for="message">Message:</label>
          <textarea v-model="updatedAdRequest.message" id="message"></textarea>
        </div>

        <div class="button-group">
          <button type="submit">Update</button>
          <button type="button" @click="close">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    adRequest: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      updatedAdRequest: { ...this.adRequest },
      influencers: []
    };
  },
  mounted() {
    this.fetchInfluencers();  // Fetch influencers when the component is mounted
  },
  methods: {
    fetchInfluencers() {
      fetch('/api/influencers/public', {
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
        console.error('Error fetching influencers:', error);
      });
    },
    close() {
      this.$emit('close');
    },
    updateAdRequest() {
      const selectedInfluencer = this.influencers.find(influencer => influencer.id === this.updatedAdRequest.influencer_id);
      fetch(`/api/ad-requests/${this.updatedAdRequest.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
         body: JSON.stringify({
            ...this.updatedAdRequest,
            influencer_name: selectedInfluencer.username,  // Pass the influencer name instead of ID
          })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to update ad request');
        }
        this.$emit('update');
        this.close();
      })
      .catch(error => {
        console.error('Error:', error);
        alert('There was a problem updating the ad request.');
      });
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
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  min-width: 300px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.ad-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 12px;
  width: 100%;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
  min-height: 50px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 5px;
  font-size: 16px;
}

button[type="submit"] {
  background-color: #4CAF50;
  color: white;
}

button[type="submit"]:hover {
  background-color: #45a049;
}

button[type="button"] {
  background-color: #f44336;
  color: white;
}

button[type="button"]:hover {
  background-color: #e53935;
}
</style>
