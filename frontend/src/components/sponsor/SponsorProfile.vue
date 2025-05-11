<template>
  <SponsorHeader></SponsorHeader>
  <div class="sponsor-profile">
    <section class="profile-content">
      <h2>Sponsor Profile Details</h2>
      <form @submit.prevent="saveChanges">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="sponsor.username" type="text" disabled>
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input v-model="password" type="password" placeholder="New password">
        </div>
        <div class="form-group">
          <label>Company Name:</label>
          <input v-model="sponsor.company_name" type="text">
        </div>
        <div class="form-group">
          <label>Industry:</label>
          <input v-model="sponsor.industry" type="text">
        </div>
        <div class="form-group">
          <label>Net Worth:</label>
          <input v-model="sponsor.net_worth" type="number">
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </section>
  </div>
</template>


<script>
import SponsorHeader from './SponsorHeader.vue';
export default {
  components:{SponsorHeader},
  data() {
    return {
      sponsor: {},
      password: ''
    };
  },
  mounted() {
    this.fetchSponsorDetails();
  },
  methods: {
    fetchSponsorDetails() {
      fetch('/api/sponsor/profile', {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        this.sponsor = data;
      })
      .catch(error => console.error('Error fetching sponsor details:', error));
    },
    saveChanges() {
        const dataToSend = {
            username: this.sponsor.username, // Username might be displayed but not editable
            company_name: this.sponsor.company_name,
            industry: this.sponsor.industry,
            net_worth: this.sponsor.net_worth,
        };
        if (this.password) {
            dataToSend.password = this.password;
        }
        fetch('/api/sponsor/update-profile', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
            })
            .then(response => {
            // Convert to JSON and preserve the response object for status checking
            return response.json().then(data => ({
                data: data,
                ok: response.ok
            }));
            })
            .then(result => {
            alert(result.data.message); // Now use result.data and result.ok
            if (result.ok) {
                this.password = ''; // Clear password field on successful update
            }
            })
            .catch(error => {
            console.error('Error updating profile:', error);
            });
        }
  }
};
</script>

<style scoped>
.sponsor-profile {
  height: 100vh;
  background-image: url('@/assets/img1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.profile-content {
  width: 400px;
  margin: auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-radius: 10px; /* Optional: Adds rounded corners to the form area */
}

.form-group {
  margin-bottom: 10px;
}
.form-group label {
  display: block;
}
input[type="text"], input[type="password"], input[type="number"] {
  width: 100%;
  padding: 8px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
