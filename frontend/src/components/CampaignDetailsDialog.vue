<template>
  <div v-if="visible" class="dialog-overlay" @click.self="close">
    <div class="dialog" role="dialog" aria-labelledby="dialogTitle">
      <h2 id="dialogTitle">Campaign Details</h2>
      <p><strong>Campaign Name:</strong> {{ campaign.name }}</p>
      <p><strong>Company Name:</strong> {{ campaign.company_name }}</p>
      <p><strong>Industry:</strong> {{ campaign.company_industry }}</p>
      <p><strong>Net Worth:</strong> {{ campaign.company_net_worth }}</p>
      <p><strong>Description:</strong> {{ campaign.description || 'N/A' }}</p>
      <p><strong>Start Date:</strong> {{ campaign.start_date }}</p>
      <p><strong>End Date:</strong> {{ campaign.end_date }}</p>
      <p><strong>Budget:</strong> ${{ campaign.budget }}</p>
      <button @click="close">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    campaign: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
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
  max-width: 600px;
  min-width: 300px;
}
</style>
