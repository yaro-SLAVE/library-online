<template>
  <tr :class="{ 'highlight-blue': shouldHighlight }">
    <td>{{ reader.id }}</td>
    <td>{{ reader.user.fullname }}</td>
    <td>{{ reader.total_books_ordered }}</td>
    <td>{{ reader.total_orders }}</td>
    <td>{{ reader.cancelled_orders }}</td>
  </tr>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface ReaderUser {
  first_name: string;
  last_name: string;
  fullname: string;
  username: string;
  department: string;
  library_card: string | null;
}

interface ReaderData {
  id: number;
  user: ReaderUser;
  total_books_ordered: number;
  total_orders: number;
  completed_orders: number;
  cancelled_orders: number;
}

const props = defineProps<{
  reader: ReaderData;
}>();

const shouldHighlight = computed<boolean>(() => {
  // подсвечиваем читателей с большим количеством отмененных заказов
  return props.reader.cancelled_orders > 1;
});
</script>

<style scoped>
.highlight-blue {
  background-color: var(--color-primary-200);
  
  td {
    background-color: var(--color-primary-200);
  }
}
</style>