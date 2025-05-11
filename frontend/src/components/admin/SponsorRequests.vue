<template>
  <div class="sponsor-requests">
    <AdminHeader></AdminHeader>
    <div class="request-list">
      <h2>Sponsor Requests</h2>
      <div v-for="request in sponsorRequests" :key="request.id" class="request-box">
        <h3>{{ request.username }}</h3>
        <p><strong>UserName:</strong> {{ request.username }}</p>
        <p><strong>Company Name:</strong> {{ request.company_name }}</p>
        <p><strong>Industry:</strong> {{ request.industry }}</p>
        <p><strong>Budget:</strong> ${{ request.net_worth }}</p>
        <button class="btn btn-success" @click="acceptRequest(request.id)">Accept</button>
        <button class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>
      </div>
    </div>
  </div>
</template>

<script>
import AdminHeader from './AdminHeader.vue';

export default {
  components: {
    AdminHeader
  },
  data() {
    return {
      sponsorRequests: []  // This will be fetched from the backend
    };
  },
  mounted() {
    this.fetchSponsorRequests();
  },
  methods: {
    fetchSponsorRequests() {
        fetch('/api/sponsor-requests', {
            headers: {
                'Authorization': `Bearer ${this.$store.state.token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();  // Parse JSON only if the response was ok
            } else {
                // If response is not ok, throw an error with the status text
                throw new Error(`Failed to fetch: ${response.statusText}`);
            }
        })
        .then(data => {
            this.sponsorRequests = data;  // Set the sponsor requests data on successful fetch
        })
        .catch(error => {
            console.error('Error fetching sponsor requests:', error);
        });
    },
    acceptRequest(id) {
      this.updateRequestStatus(id, 'accepted');
    },
    rejectRequest(id) {
      this.updateRequestStatus(id, 'rejected');
    },
    updateRequestStatus(id, status) {
      fetch(`/api/update-sponsor-status/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
      })
      .then(response => {
        if (response.ok) {
          this.fetchSponsorRequests();  // Refresh the list after updating status
        } else {
          alert('Failed to update status.');
        }
      });
    }
  }
};
</script>

<style scoped>
.sponsor-requests {
  padding: 20px;
  height: 100vh;
  background-image: url('@/assets/img1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.request-list {
  margin: 1rem;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f8f9fa;
}
.request-box {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  background-color: white;
  border-radius: 5px;
  margin-bottom: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.request-box:last-child {
  border-bottom: none;
}
.btn-success, .btn-danger {
  margin-top: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-success {
  background-color: #28a745;
  color: white;
  margin-right: 10px;
}
.btn-success:hover {
  background-color: #218838;
}
.btn-danger {
  background-color: #dc3545;
  color: white;
}
.btn-danger:hover {
  background-color: #c82333;
}
</style>
