<template>
  <SurfaceCard class="order-card">
    <div class="order-header">
      <span class="order-number">📦 Заказ #{{ num }} oт {{ orderedDate }}</span>
      <span class="order-status" :class="statusClass"
        >● {{ orderStatuses[currentStatus] }} {{ lastStatusDate }}</span
      >
    </div>
    <div class="book-list">
      <div v-for="(orderBook, index) in order.books" :key="orderBook.book.id" class="book-item">
        <div class="book-info">
          <div class="col">
            <ShortBookCard :book="orderBook.book" />
          </div>
          <StyledButton
            @click="onAddToOrderClick(orderBook.book)"
            theme="secondary"
            v-if="canReorder"
          >
            Заказать еще раз
          </StyledButton>
        </div>

        <hr v-if="index < order.books.length - 1" class="divider" />
      </div>
    </div>
    <div class="order-actions-footer" v-if="showOrderActions">
      <StyledButton theme="accent" @click="onCancelOrderClick" v-if="canCancelOrder"
        >Отказаться
      </StyledButton>
    </div>
  </SurfaceCard>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { OrderStatusEnum, Order, Book } from "@api/types";
import { orderStatuses } from "@api/types";
import { useOrderStore } from "@reader/store/orderStore";
import ShortBookCard from "@components/ShortBookCard.vue";
import StyledButton from "@components/StyledButton.vue";
import SurfaceCard from "@components/SurfaceCard.vue";
import { useFormattedDate } from "@reader/composables/useFormattedDate";

const allowedCancelStatuses: OrderStatusEnum[] = ["new", "processing", "ready"];
const notAllowedToReOrderBoookStatuses: OrderStatusEnum[] = ["new"];
const orderStore = useOrderStore();

const { order, num } = defineProps<{
  order: Order;
  num: number;
}>();

const emit = defineEmits<{
  (e: "cancel", orderId: number): number;
}>();

const { formatDate } = useFormattedDate();

const canCancelOrder = computed(() => allowedCancelStatuses.includes(currentStatus.value));

const canReorder = computed(() => !notAllowedToReOrderBoookStatuses.includes(currentStatus.value));
const showOrderActions = computed(() => canCancelOrder.value);

const orderedDate = formatDate(order.statuses[0].date);
const lastStatusDate = formatDate(order.statuses[order.statuses.length - 1].date);

const currentStatus = computed(() => {
  const lastStatus = order.statuses[order.statuses.length - 1]?.status;
  return lastStatus;
});

const statusClass = computed(() => {
  const status = currentStatus.value as OrderStatusEnum;
  return {
    [status]: true,
  };
});

async function onCancelOrderClick() {
  emit("cancel", order.id);
}

const onAddToOrderClick = (bookToOrder: Book) => {
  const isInCurrentOrder = orderStore.selectedBooks.some((book) => {
    return book.id === bookToOrder.id;
  });
  if (isInCurrentOrder) {
    return;
  } else {
    orderStore.addBook(bookToOrder);
  }
};
</script>

<style scoped lang="scss">
.order-card {
  transition:
    transform 0.2s ease,
    box-shadow 0.3s ease;
  margin: 1rem 0;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-primary-800);
}

.order-number {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-primary-800);
}

.order-status {
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 16px;
  background: var(--color-primary-800);
}

.order-status.new {
  color: var(--color-status-new);
  background: var(--background-status-new);
}

.order-status.processing {
  color: var(--color-status-processing);
  background: var(--background-status-processing);
}

.order-status.ready {
  color: var(--color-status-ready);
  background: var(--background-status-ready);
}

.order-status.done {
  color: var(--color-status-done);
  background: var(--background-status-done);
}

.order-status.cancelled {
  color: var(--color-status-cancelled);
  background: var(--background-status-cancelled);
}

.order-status.error {
  color: var(--color-status-error);
  background: var(--background-status-error);
}

.order-status.archived {
  color: var(--color-status-archived);
  background: var(--background-status-archived);
}

.book-list {
  display: flex;
  flex-direction: column;
}

.book-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.book-item {
  position: relative;
}

.order-actions-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid var(--color-primary-800);
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
</style>
