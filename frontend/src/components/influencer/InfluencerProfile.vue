<template>
<InfluencerHeader></InfluencerHeader>
  <div class="influencer-profile">
    
    <section>
      <h2>Influencer Profile Details</h2>
      <form @submit.prevent="saveChanges" class="profile-form">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="user.username" disabled>
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input type="password" v-model="user.password">
        </div>
        <div class="form-group">
          <label>Name:</label>
          <input v-model="user.name">
        </div>
        <div class="form-group">
          <label>Category:</label>
          <input v-model="user.category">
        </div>
        <div class="form-group">
          <label>Niche:</label>
          <input v-model="user.niche">
        </div>
        <div class="form-group">
          <label>Reach:</label>
          <input v-model="user.reach" type="number">
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </section>
  </div>
</template>

<script>
import InfluencerHeader from './InfluencerHeader.vue';
export default {
  components: {InfluencerHeader},
  data() {
    return {
      user: {}  // Initialize user data
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    fetchUserProfile() {
        console.log('Token:', this.$store.state.token); // This will show you what token is being sent
        fetch('/api/influencer/profile', {
            headers: {
                'Authorization': `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            this.user = data;
        })
        .catch(error => {
            console.error('Error fetching profile:', error);
        });
    },

    saveChanges() {
      fetch('/api/influencer/update-profile', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.user)
      })
      .then(response => {
        if (response.ok) {
          alert('Profile updated successfully!');
        } else {
          alert('Failed to update profile.');
        }
      })
      .catch(error => console.error('Error updating profile:', error));
    }
  }
};
</script>

<style scoped>
.influencer-profile {
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  padding: 20px;
}
.influencer-profile h2{
  color:white;
}

.influencer-profile header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2c3e50;
  padding: 1rem;
  color: white;
}
.influencer-profile nav button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
}
.influencer-profile nav button:hover {
  background-color: #2980b9;
}
.profile-form {
  display: flex;
  flex-direction: column;
  max-width: 400px;
  margin: auto;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  font-weight: bold;
  color:white;
}
.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-group input[disabled] {
  background-color: grey;
  color: black;
}
button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
