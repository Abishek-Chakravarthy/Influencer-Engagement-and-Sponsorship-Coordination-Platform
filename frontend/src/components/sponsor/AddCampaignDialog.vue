<template>
  <div class="dialog-background">
    <div class="dialog">
      <h2>Create Your Campaign</h2>
      <form @submit.prevent="submitCampaign" class="form-layout">
        <label>Name:</label>
        <input v-model="newCampaign.name" placeholder="Campaign name" required>

        <label>Description (Optional):</label>
        <textarea v-model="newCampaign.description" placeholder="Brief description (optional)"></textarea>

        <label>Start Date:</label>
        <input type="date" v-model="newCampaign.start_date" required>

        <label>End Date:</label>
        <input type="date" v-model="newCampaign.end_date" required>

        <label>Budget:</label>
        <input type="number" v-model="newCampaign.budget" placeholder="Total budget" required>

        <label>Visibility:</label>
        <select v-model="newCampaign.visibility" required>
          <option disabled value="">Please select one</option>
          <option value="Public">Public</option>
          <option value="Private">Private</option>
        </select>

        <label>Goals (Optional):</label>
        <textarea v-model="newCampaign.goals" placeholder="Main objectives (optional)"></textarea>

        <div class="button-group">
          <button type="submit" class="submit-button">Create Campaign</button>
          <button type="button" @click="$emit('close')" class="cancel-button">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>



<script>
export default {
  data() {
    return {
      newCampaign: {
        name: '',
        description: null, // Default to null if not provided
        start_date: '',
        end_date: '',
        budget: 0,
        visibility: '', // Make sure a selection is made
        goals: null, // Default to null if not provided
        amount_spent: 0, // Defaulted to 0
        flagged: false // Defaulted to false
      }
    };
  },
  methods: {
    submitCampaign() {
      if (this.newCampaign.description === '') {
        this.newCampaign.description = null;
      }
      if (this.newCampaign.goals === '') {
        this.newCampaign.goals = null;
      }

      fetch('/api/sponsor/campaigns', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.newCampaign)
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(text => { throw new Error(text.message || 'Error submitting the campaign') });
        }
        return response.json();
      })
      .then(() => {
        alert('Campaign created successfully');
        this.$emit('close'); // Close the dialog on success
        this.$parent.fetchCampaigns(); // Optionally refresh the list of campaigns
      })
      .catch(error => {
        console.error('Error:', error);
        alert(error.message || 'Error creating campaign.');
      });
    }
  }
};

</script>

<style scoped>
.dialog-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* Darker background */
  display: flex;
  justify-content: center;
  align-items: center;
}
.dialog {
  background: white;
  padding: 20px;
  width: 500px; /* Fixed width */
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* Soft shadow for depth */
}
.form-layout {
  display: flex;
  flex-direction: column;
}
.form-layout label {
  font-weight: bold; /* Make labels bold */
  margin-top: 10px;
}
.form-layout input[type="text"],
.form-layout input[type="date"],
.form-layout input[type="number"],
.form-layout textarea {
  padding: 8px;
  margin-top: 2px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
.submit-button, .cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.submit-button {
  background-color: #4CAF50;
  color: white;
}
.cancel-button {
  background-color: #f44336;
  color: white;
}
.submit-button:hover {
  background-color: #45a049;
}
.cancel-button:hover {
  background-color: #d32f2f;
}
</style>
