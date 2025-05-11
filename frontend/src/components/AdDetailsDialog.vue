<template>
  <div class="dialog-overlay" @click.self="close">
    <div class="dialog">
      <h2>Ad Request Details</h2>
      <div v-if="role === 'sponsor'">
        <p>Campaign name: {{ adDetails.campaign_name }}</p>
        <p>Influencer Name: {{ adDetails.influencer_name }}</p>
        <p>Influencer Category: {{ adDetails.category }}</p>
        <p>Influencer Niche: {{ adDetails.niche }}</p>
        <p>Influencer Reach: {{ adDetails.reach }}</p>
        <p>Messages: {{ adDetails.messages }}</p>
        <p>Payment Expected: ${{ adDetails.payment_amount }}</p>
        
        <button class="negotiate-btn" @click="toggleNegotiation">Negotiate</button>
        <button class="reject-btn" @click="rejectAd">Reject</button>
        <div v-if="showNegotiation">
          <input v-model="negotiation.payment_amount" placeholder="Payment Offered">
          <input v-model="negotiation.messages" placeholder="Message to Influencer">
          <button class="send-btn" @click="sendNegotiation">Send Negotiation</button>
        </div>
      </div>
      <div v-else-if="role === 'influencer'">
        <p>Campaign Name: {{ adDetails.campaign_name }}</p>
        <p>Ad Name: {{ adDetails.ad_name }}</p>
        <p>Ad Description: {{ adDetails.ad_desc }}</p>
        <p>Ad Terms: {{ adDetails.ad_terms }}</p>
        <p>Company Name: {{ adDetails.company_name }}</p>
        <p>Company Industry: {{ adDetails.industry }}</p>
        <p>Company Networth: ${{ adDetails.net_worth }}</p>
        <p>Sponsor Messages: {{ adDetails.messages }}</p>
        <p>Payment Offered: ${{ adDetails.payment_amount }}</p>
        
        <button class="negotiate-btn" @click="toggleNegotiation">Negotiate</button>
        <button class="reject-btn" @click="rejectAd">Reject</button>
        <div v-if="showNegotiation">
          <input v-model="negotiation.payment_amount" placeholder="Payment Expected">
          <input v-model="negotiation.messages" placeholder="Message to Sponsor">
          <button class="send-btn" @click="sendNegotiation">Send Negotiation</button>
        </div>
      </div>
      <button @click="close">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['adRequestId', 'role'],
  data() {
    return {
      adDetails: {},
      negotiation: {
        payment_amount: '',
        messages: ''
      },
      showNegotiation: false
    };
  },
  methods: {
    fetchAdDetails() {
      
      fetch(`/api/ad-requests-details/${this.adRequestId}`, {
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        console.log("Data received:", data); 
        this.adDetails = data;
        this.negotiation.payment_amount = data.payment_amount;
        this.negotiation.messages = data.messages;
      })
      .catch(error => {
        console.error('Error fetching ad details:', error);
        alert('Failed to fetch ad details.');
      });
    },
    acceptAd() {
      const url = this.role === 'sponsor' ? '/api/sponsor/ad-request/accept/' : '/api/influencer/ad-request/accept/';
      fetch(url + this.adRequestId, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(() => {
        alert('Ad request accepted.');
        this.close();
      });
    },
    sendNegotiation() {
      const url = this.role === 'sponsor' ? '/api/sponsor/ad-request/negotiate/' : '/api/influencer/ad-request/negotiate/';
      fetch(url + this.adRequestId, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          payment_amount: this.negotiation.payment_amount,
          messages: this.negotiation.messages,
          status: 'negotiated',
          req_by: this.role
        })
      }).then(() => {
        alert('Negotiation details sent.');
        this.close();
      }).catch(error => {
        console.error('Error during negotiation:', error);
        alert('Failed to send negotiation details.');
      });
    },
    toggleNegotiation() {
      this.showNegotiation = !this.showNegotiation;
    },
    rejectAd() {
      const url = this.role === 'sponsor' ? '/api/sponsor/ad-request/reject/' : '/api/influencer/ad-request/reject/';
      fetch(url + this.adRequestId, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this.$store.state.token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(() => {
        alert('Ad request rejected.');
        this.close();
      });
    },
    close() {
      this.$emit('close');
    }
  },
  mounted() {
    this.fetchAdDetails();
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
  border-radius: 10px;
  width: 80%;
  max-width: 500px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}
button {
  margin: 10px;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}
button:hover {
  transform: translateY(-2px);
}
.accept-btn {
  background-color: #4CAF50;
  color: white;
}
.accept-btn:hover {
  background-color: #45a049;
}
.negotiate-btn {
  background-color: #3498db;
  color: white;
}
.negotiate-btn:hover {
  background-color: #2980b9;
}
.reject-btn {
  background-color: #e74c3c;
  color: white;
}
.reject-btn:hover {
  background-color: #c0392b;
}
.send-btn {
  background-color: #f39c12;
  color: white;
  margin-top: 10px;
}
.send-btn:hover {
  background-color: #e67e22;
}
input {
  display: block;
  width: calc(100% - 24px);
  margin: 10px auto;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>