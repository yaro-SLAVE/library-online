<template>
  <ModalDialog v-model="loading" :esc-closeable="false">
    <div class="flex flex-col items-center">
      <LoadingSpinner />
      <p>Загрузка данных...</p>
    </div>
  </ModalDialog>
</template>

<script setup lang="ts">
import LoadingSpinner from "./LoadingSpinner.vue";
import ModalDialog from "./ModalDialog.vue";
const loading = defineModel<boolean>({ required: true });
</script>
