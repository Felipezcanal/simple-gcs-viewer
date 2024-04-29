<script setup>

import Image from './Image.vue'
import Folder from './Folder.vue'
import Modal from './Modal.vue'
import { ref, watch, computed } from 'vue'

const props = defineProps({
  path: String,
  updatePath: Function,
})
const folder = ref()
const count = ref(0)
const selectedToDownload = ref([])
const buttonDownloading = ref(0)
const showModal = ref(false)
const modalSelected = ref('')
const searchText = ref('')

function toggleSelectedToDownload(file) {
  if (selectedToDownload.value.includes(file)) {
    selectedToDownload.value.splice(selectedToDownload.value.indexOf(file), 1)
  } else {
    selectedToDownload.value = selectedToDownload.value.concat(file)
  }
}

function rstrip(str, char) {
  if (str.charAt(str.length - 1) === char) {
    return str.substring(0, -1);
  }
  return str;
}

function lstrip(str, char) {
  if (str.charAt(0) === char) {
    return str.substring(1);
  }
  return str;
}

function getData() {
  fetch(import.meta.env.VITE_API_URL + '/list',
  {
    method: 'POST',
    body: JSON.stringify({
    path: props.path,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    }
  })
  .then(response => response.json())
  .then(data => folder.value = data);
}
getData()

async function updateAll(prefix) {
  const value = props.path + prefix + '/'
  const value_stripped = lstrip(value, '/')
  await props.updatePath(value_stripped)
  getData()
}

async function updateAllAbsolute(prefix) {
  let value = ''
  if (prefix != '') {
    let index = props.path.indexOf(prefix);
    let result = props.path.substring(0, index);
    value = result + prefix + '/'
  } else {
    value = prefix + '/'
  }
  const value_stripped = lstrip(value, '/')
  await props.updatePath(value_stripped)
  getData()
}

function downloadSelected() {
  buttonDownloading.value = 1
  fetch(import.meta.env.VITE_API_URL + '/download',
  {
    method: 'POST',
    body: JSON.stringify({
    paths: selectedToDownload.value,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    }
  })
  .then(response => response.json())
  .then(data => buttonDownloading.value = false);
}

function showImageModal(image) {
  modalSelected.value = image
  showModal.value = true
}

function closeModal()
{
  showModal.value = false
}

const filteredImages = computed(() => {
  if (searchText.value == '') {
    return folder?.value?.objects
  }
  return folder?.value?.objects.filter((value) => value.includes(searchText.value))
})

const basePath = ref(import.meta.env.VITE_BASE_GCS_PATH)
if (!basePath.value.endsWith('/')) {
  basePath.value += '/'
}
const basePathPieces = basePath.value.split('/')

</script>



<template>
  <div class="input-group">
    <label for="search">Filter by image names:</label>
    <input id="search" v-model="searchText" placeholder="Filter" required />
  </div>

  <div class="container">
    <button @click.prevent="downloadSelected()" class="item2 button">
      <span v-if="buttonDownloading">Downloading...</span>
      <span v-else>Download Selected</span>
    </button>
    <h3> </h3>
    <div class="container flex flex-wrap">
      <div v-for="piece in path.split('/')" :key="piece">
        <span v-if="!basePathPieces.includes(piece)">></span>
        <button v-if="!basePathPieces.includes(piece)" @click.prevent="updateAllAbsolute(piece)" class="item2 button">{{ piece }}</button>
      </div>
    </div>

    <div class="card">
      <section class="container flex flex-wrap">
        <div v-for="prefix in folder?.prefixes" :key="prefix" class="item">
          <Folder :name="prefix" :updateAll="updateAll"/>
        </div>
      </section>


      <section class="container flex flex-wrap">
        <div v-for="object in filteredImages" :key="object" class="item">
          <Image v-if="object" :name="object" :path="path" :toggleSelectedToDownload="toggleSelectedToDownload" :showImageModal="showImageModal"/>
        </div>
      </section>
    </div>

    <div id="image-modal" v-if="showModal" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-body">
            <img :src="modalSelected" alt="asdf"/>
          </div>
        </div>
      </div>
    </div>
    <Modal @close="closeModal" :opened="showModal" :image="modalSelected"/>
  </div>
</template>

<style scoped>
/* Flex */
.flex {
	display: flex;
}

.flex-wrap {
	flex-wrap: wrap;
}

.flex-item-1 {
	flex: 1;
}

/* Flex Item */
.item {
	margin: 5px;
	text-align: center;
	font-size: 1.5em;
  display: flex;
  flex-direction: column;
  max-width: 192px;
}
.item.selected {
	background: rgb(146, 175, 135);
}

.container {
	width: 100%;
	margin: 0 auto;
}
.button {
  font-size: small;
  width: 163px;
}
.image {
  width: 163px;
  height: 163px;
}
.span {
  font-size: small;
}

/* .modal {
  z-index: 10;
  position: absolute;

}
.container {
  position: absolute;
} */


.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: calc(40% - 22px); /* Adjust width for padding */
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
