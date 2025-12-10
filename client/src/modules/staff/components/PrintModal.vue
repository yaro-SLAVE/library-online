<template>
  <div v-if="open" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Заказ #{{ props.order.id }}</h2>
        <button class="close-button" @click="open = false">×</button>
      </div>
      <div class="main-content">
        <div class="qr-container">
          <QrcodeVue :value="props.order.user.library_card?.toString()" :size="qrSize" />
        </div>
        <div class="books-section">
          <h3>Книги ({{ props.order.books.length }})</h3>
          <div class="books-list">
            <div v-for="book in props.order.books" :key="book.id" class="book">
              <ShortBookCard :book="book.book" :truncate="true" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed } from "vue";
import QrcodeVue from "qrcode.vue";
import type { Order } from "@api/types";
import ShortBookCard from "@components/ShortBookCard.vue";
// import VueHtmlToPaper from "vue-html-to-paper";

const qrSize = computed(() => {
  const minSize = 300;
  const maxSize = Math.min(window.innerWidth, window.innerHeight) * 0.5;
  return Math.max(minSize, maxSize - 100);
});

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

.qr-container {
  margin: auto;
  height: fit-content;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #eee;
}

.main-content {
  padding: 2rem;
  display: flex;
  gap: 2rem;
  .books-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1rem;

    .books-list {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;

      .book {
        padding: 1rem;
        background-color: var(--color-background-100);
        border-radius: 1em;
      }
    }
  }
}
</style>
