<template>
  <tr :class="{ 'highlight-blue': shouldHighlight }">
    <td>{{ reader.id }}</td>
    <td>{{ reader.fullname }}</td>
    <td>{{ reader.department }}</td>
    <td>{{ reader.total_books_ordered }}</td>
    <td>{{ reader.total_orders }}</td>
    <td>{{ reader.cancelled_orders }}</td>
  </tr>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface ReaderData {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  fullname: string;
  department: string;
  library_card: string | null;
  campus_id: string | null;
  mira_id: string | null;
  total_books_ordered: number;
  total_orders: number;
  completed_orders: number;
  cancelled_orders: number;
  active_orders: number;
  last_order_date: string | null;
}

const props = defineProps<{
  reader: ReaderData;
}>();

const shouldHighlight = computed<boolean>(() => {
  // подсвечиваем читателей с большим количеством отмененных заказов
  // или с просроченными книгами (если бы была такая информация)
  return props.reader.cancelled_orders > 1 || props.reader.active_orders > 3;
});
</script>

<style scoped>
.highlight-blue {
  background-color: var(--color-primary-100);
  
  td {
    background-color: var(--color-primary-100);
    border-bottom: 1px solid var(--color-primary-300);
  }
}
</style>