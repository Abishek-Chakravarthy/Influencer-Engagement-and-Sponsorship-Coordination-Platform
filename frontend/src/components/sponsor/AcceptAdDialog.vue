<template>
  <div class="dialog-overlay" @click.self="close">
    <div class="dialog">
      <h2>Accept Ad Request</h2>
      <form @submit.prevent="acceptAd">
        <div>
          <label for="ad_name">Ad Name:</label>
          <input id="ad_name" v-model="adDetails.ad_name" required>
        </div>
        <div>
          <label for="ad_desc">Ad Description:</label>
          <textarea id="ad_desc" v-model="adDetails.ad_desc" required></textarea>
        </div>
        <div>
          <label for="ad_terms">Ad Terms:</label>
          <textarea id="ad_terms" v-model="adDetails.ad_terms" required></textarea>
        </div>
        <button type="submit" class="done-btn">Done</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: ['requestId'],
  data() {
    return {
      adDetails: {
        ad_name: '',
        ad_desc: '',
        ad_terms: ''
      }
    };
  },
  methods: {
    acceptAd() {
      const url = `/api/sponsor/ad-request/accept/${this.requestId}`;
      const payload = {
        ...this.adDetails,
        status: 'accepted'
      };
      fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.close();
      })
      .catch(error => {
        console.error('Error accepting ad request:', error);
        alert('Error processing request.');
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
.done-btn {
  display: block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
.done-btn:hover {
  background-color: #45a049;
}
</style>
