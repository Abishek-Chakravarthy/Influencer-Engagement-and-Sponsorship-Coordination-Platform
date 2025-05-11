<template>
  <InfluencerHeader></InfluencerHeader>
  <div class="influencer-stats">
    
    <section class="stats-section">
      <div class="chart-container">
        <div class="chart-item">
          <h2>Revenue Analysis</h2>
          <canvas id="revenueAnalysisChart"></canvas>
        </div>
        <div class="chart-item">
          <h2>Trending Campaigns</h2>
          <canvas id="trendingCampaignsChart"></canvas>
        </div>
      </div>
      <div class="chart-container">
        <div class="chart-item">
          <h2>Company Average Ad Pay</h2>
          <div class="dropdown">
            <label for="attributeSelect">Select Attribute:</label>
            <select id="attributeSelect" v-model="selectedCompanyAttribute" @change="fetchCompanyAvgAdPay">
              <option value="company_name">Company Name</option>
              <option value="industry">Industry</option>
            </select>
          </div>
          <canvas id="companyAvgAdPayChart"></canvas>
        </div>
        <div class="chart-item">
          <h2>Most Active Influencers</h2>
          <canvas id="mostActiveInfluencersChart"></canvas>
        </div>
      </div>
    </section>
  </div>
</template>


<script>
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, BarElement, CategoryScale, LinearScale, LineController, BarController, PointElement } from 'chart.js'
import InfluencerHeader from './InfluencerHeader.vue'

ChartJS.register(Title, Tooltip, Legend, LineElement, BarElement, CategoryScale, LinearScale, LineController, BarController, PointElement)

export default {
  components: {
    InfluencerHeader
  },
  data() {
    return {
      revenueData: [],
      trendingCampaignsData: [],
      companyAvgAdPayData: [],
      mostActiveInfluencersData: [],
      selectedCompanyAttribute: 'company_name',
      revenueChart: null,
      trendingCampaignsChart: null,
      companyAvgAdPayChart: null,
      mostActiveInfluencersChart: null
    }
  },
  mounted() {
    this.fetchRevenueData()
    this.fetchTrendingCampaignsData()
    this.fetchCompanyAvgAdPay()
    this.fetchMostActiveInfluencersData()
  },
  beforeUnmount() {
    // Destroy existing chart instances before the component is destroyed
    if (this.revenueChart) this.revenueChart.destroy()
    if (this.trendingCampaignsChart) this.trendingCampaignsChart.destroy()
    if (this.companyAvgAdPayChart) this.companyAvgAdPayChart.destroy()
    if (this.mostActiveInfluencersChart) this.mostActiveInfluencersChart.destroy()
  },
  methods: {
    async fetchRevenueData() {
      try {
        const response = await fetch('/api/influencer/stats/revenue-analysis', {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        })
        const data = await response.json()
        if (Array.isArray(data)) {
          this.renderRevenueChart(data)
        } else {
          console.error('Invalid data format for revenue analysis:', data)
        }
      } catch (error) {
        console.error('Error fetching revenue data:', error)
      }
    },
    async fetchTrendingCampaignsData() {
      try {
        const response = await fetch('/api/influencer/stats/trending-campaigns', {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        })
        const data = await response.json()
        if (Array.isArray(data)) {
          this.renderTrendingCampaignsChart(data)
        } else {
          console.error('Invalid data format for trending campaigns:', data)
        }
      } catch (error) {
        console.error('Error fetching trending campaigns data:', error)
      }
    },
    async fetchCompanyAvgAdPay() {
      try {
        const response = await fetch(`/api/influencer/stats/company-avg-ad-pay?attribute=${this.selectedCompanyAttribute}`, {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        })
        const data = await response.json()
        if (Array.isArray(data)) {
          this.renderCompanyAvgAdPayChart(data)
        } else {
          console.error('Invalid data format for company avg ad pay:', data)
        }
      } catch (error) {
        console.error('Error fetching company avg ad pay data:', error)
      }
    },
    async fetchMostActiveInfluencersData() {
      try {
        const response = await fetch('/api/influencer/stats/most-active-influencers', {
          headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
        })
        const data = await response.json()
        if (Array.isArray(data)) {
          this.renderMostActiveInfluencersChart(data)
        } else {
          console.error('Invalid data format for most active influencers:', data)
        }
      } catch (error) {
        console.error('Error fetching most active influencers data:', error)
      }
    },
    renderRevenueChart(data) {
      const ctx = document.getElementById('revenueAnalysisChart').getContext('2d')
      if (this.revenueChart) this.revenueChart.destroy()
      this.revenueChart = new ChartJS(ctx, {
        type: 'line',
        data: {
          labels: data.map(item => item.payment_date),
          datasets: [{
            label: 'Total Earnings',
            data: data.map(item => item.total_earnings),
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
              text: 'Total Earnings Over Time',
              color: 'white' // Change title text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis text color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis text color to white
              }
            }
          }
        }
      })
    },
    renderTrendingCampaignsChart(data) {
      const ctx = document.getElementById('trendingCampaignsChart').getContext('2d')
      if (this.trendingCampaignsChart) this.trendingCampaignsChart.destroy()
      this.trendingCampaignsChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.campaign_name),
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
              text: 'Trending Campaigns',
              color: 'white' // Change title text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis text color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis text color to white
              }
            }
          }
        }
      })
    },
    renderCompanyAvgAdPayChart(data) {
      const ctx = document.getElementById('companyAvgAdPayChart').getContext('2d')
      if (this.companyAvgAdPayChart) this.companyAvgAdPayChart.destroy()
      this.companyAvgAdPayChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.label),
          datasets: [{
            label: 'Average Payment Amount',
            data: data.map(item => item.avg_payment_amount),
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
              text: `Average Ad Payment by ${this.selectedCompanyAttribute.charAt(0).toUpperCase() + this.selectedCompanyAttribute.slice(1)}`,
              color: 'white' // Change title text color to white
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis text color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis text color to white
              }
            }
          }
        }
      })
    },
    renderMostActiveInfluencersChart(data) {
      const ctx = document.getElementById('mostActiveInfluencersChart').getContext('2d')
      if (this.mostActiveInfluencersChart) this.mostActiveInfluencersChart.destroy()
      this.mostActiveInfluencersChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.influencer_name),
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
            }
          },
          scales: {
            x: {
              ticks: {
                color: 'white' // Change x-axis text color to white
              }
            },
            y: {
              ticks: {
                color: 'white' // Change y-axis text color to white
              }
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.influencer-stats {
  padding: 20px;
  background-image: url('@/assets/img1.png'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
}
.stats-section {
  margin-bottom: 40px;
}
.chart-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.chart-item {
  flex: 0 0 48%; /* Adjusts width of the charts to fit two in a row */
  margin-bottom: 20px;
}
.chart-item h2 {
  color: white; /* Change headings to white */
}
.dropdown {
  margin-bottom: 20px;
}
.dropdown label {
  color: white; /* Change Select Attribute label to white */
}
canvas {
  max-width: 100%; /* Adjust max-width to 100% of the parent container */
  height: 400px; /* Adjust height as needed */
  margin: 0 auto;
}
</style>