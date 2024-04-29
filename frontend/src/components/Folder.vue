<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  name: String,
  updateAll: Function,
})
</script>



<template>
  <img src="/folder.png" class="image item2" alt="Vite logo" />
  <button @click.prevent="updateAll(name)" class="item2 button">{{ name }}/</button>
</template>

<style scoped>
.image {
  width: 163px;
  height: 163px;
}
.button {
  font-size: small;
  width: 163px;
}
</style>
