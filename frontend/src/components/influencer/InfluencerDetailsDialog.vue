<template>
  <div v-if="visible" class="dialog-overlay" @click.self="close">
    <div class="dialog" role="dialog" aria-labelledby="dialogTitle">
      <h2 id="dialogTitle">Influencer Details</h2>
      <p><strong>Influencer Name:</strong> {{ influencer.name }}</p>
      <p><strong>Category:</strong> {{ influencer.category }}</p>
      <p><strong>Niche:</strong> {{ influencer.niche }}</p>
      <p><strong>Reach:</strong> {{ influencer.reach }}</p>
      <button @click="close">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    influencer: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    close() {
      this.$emit('close');
    }
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
  border-radius: 5px;
  width: 80%;
  max-width: 600px;
  min-width: 300px;
}
</style>
