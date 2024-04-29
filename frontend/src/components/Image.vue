<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  name: String,
  path: String,
  toggleSelectedToDownload: Function,
  showImageModal: Function
})

const imageUrl = ref(0)
const selected = ref(0)


function getImageUrl(object) {
  fetch(import.meta.env.VITE_API_URL + '/get_signed_url',
  {
    method: 'POST',
    body: JSON.stringify({
    url: props.path + props.name,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    }
  })
  .then(response => response.json())
  .then(data => imageUrl.value = data.signed_url)
}
getImageUrl()

function test(e) {
  parent = e.target.parentNode.classList.toggle('selected')
  props.toggleSelectedToDownload(props.path + props.name)
}

</script>



<template>
    <img :src="imageUrl" class="image item2" :alt="name" :title="name" @click.prevent="e => test(e)" />
    <span @click.prevent="e => showImageModal(imageUrl)" class="span">{{ name }}/</span>
</template>

<style scoped>
.image {
  width: 192px;
  height: 230px;
  object-fit: cover;
  object-position: 100% 0;
}
.span {
  font-size: small;
  text-overflow: clip;
  overflow: hidden;
}
</style>
