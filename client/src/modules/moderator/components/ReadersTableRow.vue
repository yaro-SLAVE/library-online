<template>
  <tr class="reader-row" @click="handleRowClick">
    <td>{{ reader.id }}</td>
    <td>{{ reader.fullname }}</td>
    <td>{{ reader.department }}</td>
    <td>{{ reader.total_books_ordered }}</td>
    <td>{{ reader.total_orders }}</td>
    <td>{{ reader.cancelled_orders }}</td>
  </tr>
</template>

<script setup lang="ts">
import type { ReaderStats } from "@api/types";

interface Props {
  reader: ReaderStats;
}

interface Emits {
  (e: 'row-click', reader: ReaderStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const handleRowClick = () => {
  emit('row-click', props.reader);
};
</script>

<style scoped lang="scss">
.reader-row {
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