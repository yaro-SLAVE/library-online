<template>
  <tr>
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

</script>

<style scoped>

</style>