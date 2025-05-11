<template>
  <div v-if="visible" class="dialog-overlay" @click.self="close">
    <div class="dialog" role="dialog" aria-labelledby="dialogTitle">
      <h2 id="dialogTitle">Update Campaign</h2>
      <form @submit.prevent="updateCampaign" class="form-container">
        <label for="name">Campaign Name:</label>
        <input type="text" v-model="updatedCampaign.name" id="name" required>

        <label for="description">Description:</label>
        <textarea v-model="updatedCampaign.description" id="description"></textarea>

        <label for="start_date">Start Date:</label>
        <input type="date" v-model="updatedCampaign.start_date" id="start_date" required>

        <label for="end_date">End Date:</label>
        <input type="date" v-model="updatedCampaign.end_date" id="end_date" required>

        <label for="budget">Budget:</label>
        <input type="number" v-model="updatedCampaign.budget" id="budget" required>

        <label for="visibility">Visibility:</label>
        <select v-model="updatedCampaign.visibility" id="visibility" required>
          <option value="Public">Public</option>
          <option value="Private">Private</option>
        </select>

        <div class="button-container">
          <button type="submit" class="update-btn">Update</button>
          <button type="button" @click="close" class="cancel-btn">Cancel</button>
        </div>
      </form>
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
  data() {
    return {
      updatedCampaign: { ...this.campaign }
    };
  },
  watch: {
    campaign(newVal) {
      this.updatedCampaign = { ...newVal };
    }
  },
  methods: {
    close() {
      this.$emit('close');
    },
    updateCampaign() {
      fetch(`/api/campaigns/${this.updatedCampaign.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.updatedCampaign)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to update campaign');
        }
        this.$emit('update');
        this.close();
      })
      .catch(error => {
        console.error('Error:', error);
        alert('There was a problem updating the campaign.');
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
  border-radius: 5px;
  width: 90%;
  max-width: 600px;
  min-width: 300px;
}
.form-container {
  display: flex;
  flex-direction: column;
}
label {
  margin-top: 10px;
  margin-bottom: 5px;
  font-weight: bold;
}
input[type="text"],
textarea,
input[type="date"],
input[type="number"],
select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}
textarea {
  resize: vertical;
}
.button-container {
  display: flex;
  justify-content: space-between;
}
button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.update-btn {
  background-color: #4CAF50;
  color: white;
}
.update-btn:hover {
  background-color: #45a049;
}
.cancel-btn {
  background-color: #f44336;
  color: white;
}
.cancel-btn:hover {
  background-color: #e53935;
}
</style>
