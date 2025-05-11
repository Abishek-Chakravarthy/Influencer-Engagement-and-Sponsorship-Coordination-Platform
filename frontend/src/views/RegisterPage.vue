<template>
  <div class="register-page">
    <div class="register-container">
      <h2>{{ role.charAt(0).toUpperCase() + role.slice(1) }} Register</h2>
      <form @submit.prevent="register">
        <input type="text" v-model="username" placeholder="Username" />
        <input type="password" v-model="password" placeholder="Password" />
        <input type="email" v-model="email" placeholder="Email" />
        <div v-if="role === 'influencer'">
          <input type="text" v-model="name" placeholder="Name" class="spaced-input"/>
          <input type="text" v-model="niche" placeholder="Niche" />
          <input type="text" v-model="category" placeholder="Category" class="spaced-input"/>
          <input type="number" v-model="reach" placeholder="Reach" />
        </div>
        <div v-if="role === 'sponsor'">
          <input type="text" v-model="company_name" placeholder="Company Name" class="spaced-input"/>
          <input type="text" v-model="industry" placeholder="Industry" />
          <input type="number" v-model="net_worth" placeholder="Company Net Worth" class="spaced-input"/>
        </div>
        <button type="submit">Register</button>
      </form>
      <p v-if="registrationMessage">{{ registrationMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['role'],
  data() {
    return {
      username: '',
      password: '',
      email: '',
      name: '',
      niche: '',
      category: '',
      reach: '',
      company_name: '',
      industry: '',
      net_worth: '',
      registrationMessage: '' // To display the message after registration
    };
  },
  methods: {
    async register() {
      const userData = {
        username: this.username,
        password: this.password,
        email: this.email,
        role: this.role,
        request_status: this.role === 'sponsor' ? 'pending' : 'accepted', // Default 'accepted' for influencers
        request_date: new Date().toISOString() // Send the current date
      };
      if (this.role === 'influencer') {
        Object.assign(userData, {
          name: this.name,
          niche: this.niche,
          category: this.category,
          reach: this.reach
        });
      } else if (this.role === 'sponsor') {
        Object.assign(userData, {
          company_name: this.company_name,
          industry: this.industry,
          net_worth: this.net_worth
        });
      }
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      const data = await response.json();
      if (response.ok) {
        
        if (this.role === 'sponsor') {
          this.registrationMessage = "The Admin will give you access to the platform shortly.";
        } else {
          alert('User registered successfully. You can login now.');
          this.$router.push({ name: 'login', params: { isAdmin: false } });
        }
      } else {
        alert(data.message);
      }
    }
  }
};
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.register-container {
  max-width: 500px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff; /* Set background color to white */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #34495e;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input.spaced-input {
  margin-bottom: 20px; /* Increased spacing for specific inputs */
}

button {
  padding: 10px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #218c4a;
}
</style>
