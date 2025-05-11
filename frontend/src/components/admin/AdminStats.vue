<template>
  <div class="admin-stats">
    <AdminHeader></AdminHeader>
    <section class="stats-row">
      <div class="stats-section">
        <h2>User Distribution</h2>
        <canvas id="userDistributionChart"></canvas>
      </div>
      <div class="stats-section">
        <h2>Revenue Analysis for Influencers</h2>
        <div class="dropdown">
          <label for="attributeSelect">Select Attribute:</label>
          <select id="attributeSelect" v-model="selectedAttribute" @change="fetchRevenueAnalysis">
            <option value="username">Username</option>
            <option value="category">Category</option>
            <option value="niche">Niche</option>
          </select>
        </div>
        <canvas id="revenueAnalysisChart"></canvas>
      </div>
    </section>
    <section class="stats-row">
      <div class="stats-section">
        <h2>Campaign Statistics</h2>
        <canvas id="campaignStatisticsChart"></canvas>
      </div>
      <div class="stats-section">
        <h2>Most Active Companies</h2>
        <div class="dropdown">
          <label for="companyAttributeSelect">Select Attribute:</label>
          <select id="companyAttributeSelect" v-model="selectedCompanyAttribute" @change="fetchActiveCompanies">
            <option value="company_name">Company Name</option>
            <option value="industry">Industry</option>
          </select>
        </div>
        <canvas id="mostActiveCompaniesChart"></canvas>
      </div>
    </section>
    <section class="stats-row">
      <div class="stats-section">
        <h2>Company Ad Request Statistics</h2>
        <canvas id="companyAdRequestChart"></canvas>
      </div>
      <div class="stats-section">
        <h2>Total Ad Request Statistics</h2>
        <canvas id="totalAdRequestChart"></canvas>
      </div>
    </section>
  </div>
</template>

<script>
import { Chart as ChartJS, Title, Tooltip, Legend, BarController, PieController, BarElement, ArcElement, CategoryScale, LinearScale } from 'chart.js'
import AdminHeader from './AdminHeader.vue'

ChartJS.register(Title, Tooltip, Legend, BarController, PieController, BarElement, ArcElement, CategoryScale, LinearScale)

export default {
  components: {
    AdminHeader
  },
  data() {
    return {
      userDistributionChart: null,
      revenueAnalysisChart: null,
      campaignStatisticsChart: null,
      mostActiveCompaniesChart: null,
      companyAdRequestChart: null,
      totalAdRequestChart: null,
      selectedAttribute: 'username',
      selectedCompanyAttribute: 'company_name'
    }
  },
  mounted() {
    this.fetchUserDistribution()
    this.fetchRevenueAnalysis()
    this.fetchCampaignStatistics()
    this.fetchActiveCompanies()
    this.fetchCompanyAdRequestStatistics()
    this.fetchTotalAdRequestStatistics()
  },
  beforeUnmount() {
    // Destroy existing chart instances before the component is destroyed
    if (this.userDistributionChart) this.userDistributionChart.destroy()
    if (this.revenueAnalysisChart) this.revenueAnalysisChart.destroy()
    if (this.campaignStatisticsChart) this.campaignStatisticsChart.destroy()
    if (this.mostActiveCompaniesChart) this.mostActiveCompaniesChart.destroy()
    if (this.companyAdRequestChart) this.companyAdRequestChart.destroy()
    if (this.totalAdRequestChart) this.totalAdRequestChart.destroy()
  },
  methods: {
    async fetchUserDistribution() {
      const response = await fetch('/api/admin/stats/user-distribution', {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      const data = await response.json()
      if (data) {
        this.renderUserDistributionChart(data)
      } else {
        console.error('Expected an object for user distribution data')
      }
    },
    async fetchRevenueAnalysis() {
      const response = await fetch(`/api/admin/stats/revenue-analysis?attribute=${this.selectedAttribute}`, {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      const data = await response.json()
      if (Array.isArray(data)) {
        this.renderRevenueAnalysisChart(data)
      } else {
        console.error('Expected an array for revenue analysis data')
      }
    },
    async fetchCampaignStatistics() {
      const response = await fetch('/api/admin/stats/campaign-statistics', {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      const data = await response.json()
      if (Array.isArray(data)) {
        this.renderCampaignStatisticsChart(data)
      } else {
        console.error('Expected an array for campaign statistics data')
      }
    },
    async fetchActiveCompanies() {
      const response = await fetch(`/api/admin/stats/active-companies?attribute=${this.selectedCompanyAttribute}`, {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      const data = await response.json()
      if (Array.isArray(data)) {
        this.renderActiveCompaniesChart(data)
      } else {
        console.error('Expected an array for active companies data')
      }
    },
    async fetchCompanyAdRequestStatistics() {
      const response = await fetch('/api/admin/stats/company-ad-requests', {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      const data = await response.json()
      if (Array.isArray(data)) {
        this.renderCompanyAdRequestChart(data)
      } else {
        console.error('Expected an array for company ad request statistics data')
      }
    },
    async fetchTotalAdRequestStatistics() {
      const response = await fetch('/api/admin/stats/total-ad-requests', {
        headers: { 'Authorization': `Bearer ${this.$store.state.token}` }
      })
      const data = await response.json()
      if (Array) {
        this.renderTotalAdRequestChart(data)
      } else {
        console.error('Expected an array for total ad request statistics data')
      }
    },
    renderUserDistributionChart(data) {
      if (this.userDistributionChart) {
        this.userDistributionChart.destroy()
      }
      const ctx = document.getElementById('userDistributionChart').getContext('2d')
      this.userDistributionChart = new ChartJS(ctx, {
        type: 'pie',
        data: {
          labels: ['Influencers', 'Flagged Influencers', 'Sponsors', 'Flagged Sponsors'],
          datasets: [{
            data: [data.total_influencers, data.flagged_influencers, data.total_sponsors, data.flagged_sponsors],
            backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56', '#FF9F40']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white'  // Set legend text color to white
              }
            },
            title: {
              display: true,
              text: 'User Distribution',
              color: 'white'
            }
          }
        }
      })
    },
    renderRevenueAnalysisChart(data) {
      if (this.revenueAnalysisChart) {
        this.revenueAnalysisChart.destroy()
      }
      const ctx = document.getElementById('revenueAnalysisChart').getContext('2d')
      this.revenueAnalysisChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.label),
          datasets: [{
            label: 'Total Earnings',
            data: data.map(item => item.total_earnings),
            backgroundColor: '#36A2EB'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white'  // Set legend text color to white
              }
            },
            title: {
              display: true,
              text: `Revenue Analysis by ${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)}`,
              color: 'white'
            }
          },
          scales: {
            x: {
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            },
            y: {
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            }
          }
        }
      })
    },
    renderCampaignStatisticsChart(data) {
      if (this.campaignStatisticsChart) {
        this.campaignStatisticsChart.destroy()
      }
      const ctx = document.getElementById('campaignStatisticsChart').getContext('2d')
      this.campaignStatisticsChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.name),
          datasets: [
            {
              label: 'Amount Spent',
              data: data.map(item => item.amount_spent),
              backgroundColor: '#FF6384'
            },
            {
              label: 'Remaining Budget',
              data: data.map(item => item.budget - item.amount_spent),
              backgroundColor: '#36A2EB'
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white'  // Set legend text color to white
              }
            },
            title: {
              display: true,
              text: 'Campaign Statistics',
              color: 'white'
            },
            tooltip: {
              callbacks: {
                label: function (tooltipItem) {
                  return `${tooltipItem.dataset.label}: $${tooltipItem.raw.toFixed(2)}`
                }
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            },
            y: {
              stacked: true,
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            }
          }
        }
      })
    },
    renderActiveCompaniesChart(data) {
      if (this.mostActiveCompaniesChart) {
        this.mostActiveCompaniesChart.destroy()
      }
      const ctx = document.getElementById('mostActiveCompaniesChart').getContext('2d')
      this.mostActiveCompaniesChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.label),
          datasets: [{
            label: 'Number of Accepted Ad Requests',
            data: data.map(item => item.count),
            backgroundColor: '#FFCE56'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white'  // Set legend text color to white
              }
            },
            title: {
              display: true,
              text: `Most Active Companies by ${this.selectedCompanyAttribute.charAt(0).toUpperCase() + this.selectedCompanyAttribute.slice(1)}`,
              color: 'white'
            }
          },
          scales: {
            x: {
              ticks: {
                                fontSize: 14,
                color: 'white'
              }
            },
            y: {
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            }
          }
        }
      })
    },
    renderCompanyAdRequestChart(data) {
      if (this.companyAdRequestChart) {
        this.companyAdRequestChart.destroy()
      }
      const ctx = document.getElementById('companyAdRequestChart').getContext('2d')
      this.companyAdRequestChart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.company_name),
          datasets: [
            {
              label: 'Accepted',
              data: data.map(item => item.accepted),
              backgroundColor: '#36A2EB'
            },
            {
              label: 'Pending',
              data: data.map(item => item.pending),
              backgroundColor: '#FFCE56'
            },
            {
              label: 'Negotiated',
              data: data.map(item => item.negotiated),
              backgroundColor: '#FF6384'
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white'  // Set legend text color to white
              }
            },
            title: {
              display: true,
              text: 'Company Ad Request Statistics',
              color: 'white'
            }
          },
          scales: {
            x: {
              stacked: true,
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            },
            y: {
              stacked: true,
              ticks: {
                fontSize: 14,
                color: 'white'
              }
            }
          }
        }
      })
    },
    renderTotalAdRequestChart(data) {
      if (this.totalAdRequestChart) {
        this.totalAdRequestChart.destroy()
      }
      const ctx = document.getElementById('totalAdRequestChart').getContext('2d')
      this.totalAdRequestChart = new ChartJS(ctx, {
        type: 'pie',
        data: {
          labels: ['Accepted', 'Pending', 'Negotiated'],
          datasets: [{
            data: [data.accepted, data.pending, data.negotiated],
            backgroundColor: ['#36A2EB', '#FFCE56', '#FF6384']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: 'white'  // Set legend text color to white
              }
            },
            title: {
              display: true,
              text: 'Total Ad Request Statistics',
              color: 'white'
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.admin-stats {
  padding: 20px;
  height: 300vh;
  background-image: url('@/assets/img1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.admin-stats h2 {
  color: white;
}
.stats-row {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 40px;
}
.stats-section {
  width: 48%;
}
.dropdown {
  margin-bottom: 20px;
}
.dropdown label {
  color: white;
}
canvas {
  max-width: 100%;
}
</style>

