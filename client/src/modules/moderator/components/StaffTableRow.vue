<template>
  <tr class="staff-row" @click="handleRowClick">
    <td>{{ staff.fullname }}</td>
    <td>{{ staff.department }}</td>
    <td>{{ staff.total_orders }}</td>
    <td>{{ staff.cancelled_orders }}</td>
  </tr>
</template>

<script setup lang="ts">
import type { StaffStats } from "@api/types";
import { computed } from 'vue';

interface Props {
  staff: StaffStats;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'row-click': [staff: StaffStats]
}>();

const hasOrders = computed(() => {
  return (props.staff.total_orders ?? 0) > 0;
});

const handleRowClick = () => {
  emit('row-click', props.staff);
};
</script>

<style scoped lang="scss">
.staff-row {
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
    vertical-align: middle;
  }
}
</style>