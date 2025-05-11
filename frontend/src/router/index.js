import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import AdminFind from '@/components/admin/AdminFind.vue';
import AdminStats from '@/components/admin/AdminStats.vue';
import InfluencerDashboard from '@/components/influencer/InfluencerDashboard.vue';
import InfluencerProfile from '@/components/influencer/InfluencerProfile.vue';
import InfluencerFind from '@/components/influencer/InfluencerFind.vue';
import InfluencerStats from '@/components/influencer/InfluencerStats.vue';
import SponsorDashboard from '@/components/sponsor/SponsorDashboard.vue';
import SponsorRequests from '@/components/admin/SponsorRequests.vue';
import SponsorProfile from '@/components/sponsor/SponsorProfile.vue';
import SponsorCampaigns from '@/components/sponsor/SponsorCampaigns.vue';
import SponsorFind from '@/components/sponsor/SponsorFind.vue';
import SponsorStats from '@/components/sponsor/SponsorStats.vue';
import CampaignDetails from '@/components/sponsor/CampaignDetails.vue';
import AdDetails from '@/components/AdDetailsDialog.vue';


const routes = [
    { path: '/', name: 'home', component: HomePage },
    { path: '/register/:role', name: 'register', component: RegisterPage, props: true },
    { path: '/login/:isAdmin', name: 'login', component: LoginPage, props: true },
    { path: '/admin-dashboard', name: 'admin-dashboard', component: AdminDashboard },
    { path: '/sponsor-requests', name: 'sponsor-requests', component: SponsorRequests },
    { path: '/admin-find', name: 'admin-find', component: AdminFind },
    { path: '/admin-stats', name: 'admin-stats', component: AdminStats },
    { path: '/influencer-dashboard', name: 'influencer-dashboard', component: InfluencerDashboard },
    { path: '/influencer-profile', name: 'influencer-profile', component: InfluencerProfile },
    { path: '/influencer-find', name: 'influencer-find', component: InfluencerFind },
    { path: '/influencer-stats', name: 'influencer-stats', component: InfluencerStats },
    { path: '/sponsor-dashboard', name: 'sponsor-dashboard', component: SponsorDashboard },
    { path: '/sponsor-profile', name: 'sponsor-profile', component: SponsorProfile },
    { path: '/sponsor-campaigns', name: 'sponsor-campaigns', component: SponsorCampaigns },
    { path: '/sponsor-find', name: 'sponsor-find', component: SponsorFind },
    { path: '/sponsor-stats', name: 'sponsor-stats', component: SponsorStats },
    { path: '/campaign-details/:campaignId',name: 'campaign-details',component: CampaignDetails,props: true},
    { path: '/ad-request/:requestId',name: 'ad-details',component: AdDetails,props: true}
    
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;
