<template>
    <div>
        <h3>Create New Campaign</h3>
        <form @submit.prevent="createCampaign">
            <input type="text" v-model="name" placeholder="Campaign Name" />
            <textarea v-model="description" placeholder="Description"></textarea>
            <input type="date" v-model="start_date" />
            <input type="date" v-model="end_date" />
            <input type="number" v-model="budget" placeholder="Budget" />
            <select v-model="visibility">
                <option value="public">Public</option>
                <option value="private">Private</option>
            </select>
            <button type="submit">Create</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            name: '',
            description: '',
            start_date: '',
            end_date: '',
            budget: '',
            visibility: 'public'
        };
    },
    methods: {
        async createCampaign() {
            const response = await fetch('/api/campaigns', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.$store.state.token}`
                },
                body: JSON.stringify({
                    name: this.name,
                    description: this.description,
                    start_date: this.start_date,
                    end_date: this.end_date,
                    budget: this.budget,
                    visibility: this.visibility
                })
            });
            const data = await response.json();
            if (response.ok) {
                alert('Campaign created successfully');
                // Redirect to another page or update state
            } else {
                alert(data.message);
            }
        }
    }
};
</script>
