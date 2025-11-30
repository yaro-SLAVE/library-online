<template>
  <tr class="reader-row" @click="handleRowClick">
    <td>{{ order.id }}</td>
    <td>{{ order.fullname }}</td>
    <td>{{ order.employee_collect || '-' }}</td>
    <td>{{ order.employee_issue || '-' }}</td>
    <td>{{ order.status }}</td>
  </tr>
</template>

<script setup lang="ts">
import type { OrderStats } from "@api/types";

interface Props {
  order: OrderStats;
} 

interface Emits {
  (e: 'row-click', order: OrderStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const handleRowClick = () => {
  emit('row-click', props.order);
};
</script>

<style scoped lang="scss">
.order-row {
  cursor: pointer;
  transition: background-color 0.2s;
  background-color: var(--color-background-100);
  
  &:hover {
    background-color: var(--color-background-200);
  }
  
  td {
    padding: 12px;
    text-align: left;
    color: var(--color-text-800);
    border-bottom: 1px solid var(--color-text-200);
    background-color: transparent;
  }
}
</style>
