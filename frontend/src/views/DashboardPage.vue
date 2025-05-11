<template>
    <div>
        <h2>Dashboard</h2>
        <div v-if="$store.state.user && $store.state.user.role === 'admin'">
            <AdminDashboard />
        </div>
        <div v-else-if="$store.state.user && $store.state.user.role === 'sponsor'">
            <SponsorDashboard />
        </div>
        <div v-else-if="$store.state.user && $store.state.user.role === 'influencer'">
            <InfluencerDashboard />
        </div>
    </div>
</template>

<script>
import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import SponsorDashboard from '@/components/sponsor/SponsorDashboard.vue';
import InfluencerDashboard from '@/components/influencer/InfluencerDashboard.vue';

export default {
    name: 'DashboardPage',
    components: {
        AdminDashboard,
        SponsorDashboard,
        InfluencerDashboard
    }
};
</script>
