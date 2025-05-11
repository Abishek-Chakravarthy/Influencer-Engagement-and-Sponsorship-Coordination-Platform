<template>
  <div class="dialog-overlay" @click.self="close">
    <div class="dialog">
      <h2 v-if="type === 'campaign'">Campaign Details</h2>
      <h2 v-else-if="type === 'user'">User Details</h2>
      
      <div v-if="type === 'campaign'">
        <p><strong>Campaign Name:</strong> {{ data.name }}</p>
        <p><strong>Company Name:</strong> {{ data.company_name }}</p>
        <p><strong>Description:</strong> {{ data.description }}</p>
        <p><strong>Start Date:</strong> {{ data.start_date }}</p>
        <p><strong>End Date:</strong> {{ data.end_date }}</p>
        <p><strong>Budget:</strong> ${{ data.budget }}</p>
        <p><strong>Amount Spent:</strong> ${{ data.amount_spent }}</p>
        <p><strong>Visibility:</strong> {{ data.visibility }}</p>
        <p><strong>Industry:</strong> {{ data.industry }}</p>
        <p><strong>Net Worth:</strong> ${{ data.net_worth }}</p>
      </div>
      
      <div v-else-if="type === 'user'">
        <p><strong>Username:</strong> {{ data.name }}</p>
        <p><strong>Role:</strong> {{ data.role }}</p>
        <p v-if="data.company_name"><strong>Company Name:</strong> {{ data.company_name }}</p>
        <p v-if="data.industry"><strong>Industry:</strong> {{ data.industry }}</p>
        <p v-if="data.net_worth"><strong>Net Worth:</strong> ${{ data.net_worth }}</p>
        <p v-if="data.category"><strong>Category:</strong> {{ data.category }}</p>
        <p v-if="data.earnings"><strong>Earnings:</strong> ${{ data.earnings }}</p>
        <p v-if="data.niche"><strong>Niche:</strong> {{ data.niche }}</p>
        <p v-if="data.reach"><strong>Reach:</strong> {{ data.reach }}</p>
      </div>

      <button @click="close">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      required: true
    },
    data: {
      type: Object,
      required: true
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
  max-width: 500px;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
