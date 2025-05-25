<template>
  <div v-if="open" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Заказ #{{ props.order.id }}</h2>
        <button class="close-button" @click="open = false">×</button>
      </div>
      <div class="main-content">
        <div>
          ФИО:
          {{ props.order.user.first_name }}
          {{ props.order.user.last_name }}
          {{ props.order.user.fullname }}
        </div>
        <div>
          Институт:
          {{ props.order.user.department }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type { Order } from "@api/types";
// import VueHtmlToPaper from "vue-html-to-paper";

const props = defineProps<{
  order: Order;
}>();

const open = defineModel<boolean>();
</script>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--color-background-50);
  border-radius: 0.5rem;
  width: min(100%, 56rem);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-text-200);
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-text-100);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-background-100);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.375rem;
  color: var(--color-text-800);
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-400);
  padding: 0 0.5rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-primary-600);
}

.main-content {
  padding: 2rem;
  display: flex;
  gap: 2rem;
}
</style>
