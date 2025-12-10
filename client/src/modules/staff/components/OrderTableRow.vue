<template>
  <tr :class="{ 'highlight-red': shouldHighlight }">
    <th>{{ order.id }}</th>
    <td>{{ order.user.first_name }} {{ order.user.last_name }}</td>
    <td>{{ formatDate(order.statuses[0]?.date) }}</td>
    <td>
      <button
        class="info-button"
        @click="handleOpenOrderDetails(order.id)"
        aria-label="Показать детали заказа"
      >
        Инфо
      </button>
    </td>
  </tr>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { UserOrder } from "@api/types";
import { calculateHighlightTime } from "@staff/utils/orderHighlighting";

const props = defineProps<{
  order: UserOrder;
}>();

const emit = defineEmits<{
  (e: "getOrder", id: number): void;
}>();

const orderShouldHighlightAt = computed<Date | null>(() => {
  if (
    props.order.statuses &&
    props.order.statuses.length > 0 &&
    props.order.statuses[0].status === "new" &&
    props.order.statuses.at(-1)?.status === "new"
  ) {
    return calculateHighlightTime(props.order.statuses[0].date);
  }
  return null;
});

const shouldHighlight = computed<boolean>(() => {
  if (!orderShouldHighlightAt.value) {
    return false;
  }
  const now = new Date();
  return now >= orderShouldHighlightAt.value;
});

function formatDate(dateString?: string): string {
  if (!dateString) return "---";

  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("ru-RU", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    })
      .format(date)
      .replace(",", " |");
  } catch {
    return dateString;
  }
}

const handleOpenOrderDetails = (orderId: number) => {
  emit("getOrder", orderId);
};
</script>

<style scoped>
.highlight-red {
  th {
    background-color: var(--color-accent-400);
  }
  td {
    background-color: var(--color-accent-300);
  }
}

th,
td {
  padding: 12px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}

.info-button {
  padding: 6px 12px;
  border: none;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  background-color: var(--color-primary-400);
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--color-accent-700);
  }

  &:focus-visible {
    outline: 2px solid var(--color-accent-500);
    outline-offset: 2px;
  }
}
</style>
