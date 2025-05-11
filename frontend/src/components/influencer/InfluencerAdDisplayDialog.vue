<template>
  <div class="dialog-overlay" @click.self="close">
    <div class="dialog">
      <h2>Ad Request Details</h2>
      <p>Campaign Name: {{ campaign.campaign_name }}</p>
      <p>Ad Name: {{ campaign.ad_name }}</p>
      <p>Ad Description: {{ campaign.ad_desc }}</p>
      <p>Ad Terms: {{ campaign.ad_terms }}</p>
      <p>Requirements: {{ campaign.requirements }}</p>
      <p>Messages: {{ campaign.messages }}</p>
      <p>Payment Amount: ${{ campaign.payment_amount }}</p>
      <button @click="close">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['campaign'],
  mounted() {
    console.log("Ad details received in dialog:", this.campaign); // Check if the ad details are received
  },
  methods: {
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
</style>
