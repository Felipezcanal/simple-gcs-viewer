<script setup>
import { ref, watch } from 'vue'
const props = defineProps({
  opened: Boolean,
  image: String
})
</script>



<template>
    <!-- template for the modal component -->
    <div class="modal-mask" v-if="opened">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            <button class="modal-default-button" @click="$emit('close')">
              OK
            </button>
          </div>

          <div class="modal-body">
            
            <img :src="image"/>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 80%;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  font-family: Helvetica, Arial, sans-serif;
  height: 80vh;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-body img {
  width: 30%;
}

.modal-default-button {
  display: block;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.5s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

</style>
