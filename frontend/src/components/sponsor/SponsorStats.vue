<template>
<SponsorHeader></SponsorHeader>
  <div class="sponsor-stats">
    
    <div class="stats-grid">
      <section class="stats-section">
        <h2>Total Amount Spent vs Time</h2>
        <canvas id="totalAmountSpentChart"></canvas>
      </section>
      <section class="stats-section">
        <h2>My Campaigns</h2>
        <canvas id="myCampaignsChart"></canvas>
      </section>
      <section class="stats-section">
        <h2>Most Active Companies</h2>
        <div class="dropdown">
          <label for="companyAttributeSelect">Select Attribute:</label>
          <select id="companyAttributeSelect" v-model="selectedCompanyAttribute" @change="fetchMostActiveCompanies">
            <option value="company_name">Company Name</option>
            <option value="industry">Industry</option>
          </select>
        </div>
        <canvas id="mostActiveCompaniesChart"></canvas>
      </section>
      <section class="stats-section">
        <h2>Most Active Influencers</h2>
        <canvas id="mostActiveInfluencersChart"></canvas>
      </section>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale } from 'chart.js';
import SponsorHeader from './SponsorHeader.vue';

ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale);

export default {
  components: {
    SponsorHeader,
  },
  data() {
    return {
      totalAmountSpentChart: null,
      myCampaignsChart: null,
      mostActiveCompaniesChart: null,
      mostActiveInfluencersChart: null,
      selectedCompanyAttribute: 'company_name',
    };
  },
  mounted() {
    this.fetchTotalAmountSpent();
    this.fetchMyCampaigns();
    this.fetchMostActiveCompanies();
    this.fetchMostActiveInfluencers();
  },
  methods: {
    async fetchTotalAmountSpent() {
      try {
        const response = await fetch('/api/sponsor/stats/total-amount-spent', {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        });
        const data = await response.json();
        this.renderTotalAmountSpentChart(data);
      } catch (error) {
        console.error('Error fetching total amount spent:', error);
      }
    },
    async fetchMyCampaigns() {
      try {
        const response = await fetch('/api/sponsor/stats/my-campaigns', {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        });
        const data = await response.json();
        if (data && data.length > 0) {
          this.renderMyCampaignsChart(data);
        } else {
          console.warn('No campaign data available.');
        }
      } catch (error) {
        console.error('Error fetching my campaigns:', error);
      }
    },
    async fetchMostActiveCompanies() {
      try {
        const response = await fetch(`/api/sponsor/stats/most-active-companies?attribute=${this.selectedCompanyAttribute}`, {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        });
        const data = await response.json();
        this.renderMostActiveCompaniesChart(data);
      } catch (error) {
        console.error('Error fetching most active companies:', error);
      }
    },
    async fetchMostActiveInfluencers() {
      try {
        const response = await fetch('/api/sponsor/stats/most-active-influencers', {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        });
        const data = await response.json();
        this.renderMostActiveInfluencersChart(data);
      } catch (error) {
        console.error('Error fetching most active influencers:', error);
      }
    },
    renderTotalAmountSpentChart(data) {
      if (this.totalAmountSpentChart) this.totalAmountSpentChart.destroy();
      const ctx = document.getElementById('totalAmountSpentChart').getContext('2d');
      this.totalAmountSpentChart = new ChartJS(ctx, {
        type: 'line',
        data: {
          labels: data.dates,
          datasets: [{
            label: 'Total Amount Spent',
            data: data.amounts,
            backgroundColor: '#36A2EB',
            borderColor: '#36A2EB',
            fill: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white' // Change legend text color to white
              }
            },
            title: {
              display: true,
              text: 'Total Amount Spent vs Time',
              color: 'white' // Change title text color to white
            },
            tooltip: {
              bodyColor: 'white' // Change tooltip text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis ticks color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis ticks color to white
              }
            }
          }
        }
      });
    },
    renderMyCampaignsChart(data) {
      if (this.myCampaignsChart) this.myCampaignsChart.destroy();
      const ctx = document.getElementById('myCampaignsChart').getContext('2d');
      this.myCampaignsChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(c => c.name),
          datasets: [{
            label: 'Budget',
            data: data.map(c => c.budget),
            backgroundColor: '#36A2EB',
          }, {
            label: 'Amount Spent',
            data: data.map(c => c.amount_spent),
            backgroundColor: '#FF6384',
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white' // Change legend text color to white
              }
            },
            title: {
              display: true,
              text: 'My Campaigns',
              color: 'white' // Change title text color to white
            },
            tooltip: {
              bodyColor: 'white' // Change tooltip text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis ticks color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis ticks color to white
              }
            }
          }
        }
      });
    },
    renderMostActiveCompaniesChart(data) {
      if (this.mostActiveCompaniesChart) this.mostActiveCompaniesChart.destroy();
      const ctx = document.getElementById('mostActiveCompaniesChart').getContext('2d');
      this.mostActiveCompaniesChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.label),
          datasets: [{
            label: 'Number of Accepted Ad Requests',
            data: data.map(item => item.ad_request_count),
            backgroundColor: '#36A2EB'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white' // Change legend text color to white
              }
            },
            title: {
              display: true,
              text: `Most Active Companies by ${this.selectedCompanyAttribute.charAt(0).toUpperCase() + this.selectedCompanyAttribute.slice(1)}`,
              color: 'white' // Change title text color to white
            },
            tooltip: {
              bodyColor: 'white' // Change tooltip text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis ticks color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis ticks color to white
              }
            }
          }
        }
      });
    },
    renderMostActiveInfluencersChart(data) {
      if (this.mostActiveInfluencersChart) this.mostActiveInfluencersChart.destroy();
      const ctx = document.getElementById('mostActiveInfluencersChart').getContext('2d');
      this.mostActiveInfluencersChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.username),
          datasets: [{
            label: 'Number of Ad Requests',
            data: data.map(item => item.ad_request_count),
            backgroundColor: '#36A2EB'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white' // Change legend text color to white
              }
            },
            title: {
              display: true,
              text: 'Most Active Influencers',
              color: 'white' // Change title text color to white
            },
            tooltip: {
              bodyColor: 'white' // Change tooltip text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis ticks color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis ticks color to white
              }
            }
          }
        }
      });
    }
  }
};
</script>


<style scoped>
.sponsor-stats {
  padding: 20px;
  background-image: url('@/assets/img1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
}

.stats-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.stats-section {
  flex: 1 1 calc(50% - 20px);
  box-sizing: border-box;
  margin-bottom: 20px;
}

.stats-section h2,
.dropdown label {
  color: white; /* Change headers and label to white */
}

canvas {
  max-width: 100%;
}

.dropdown label {
  color: white; /* Ensure the "Select Attribute" label is white */
}
</style>
