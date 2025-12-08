<template>
  <tr class="staff-row" @click="handleRowClick">
    <td>{{ staff.fullname }}</td>
    <td>{{ staff.total_orders }}</td>
    <td>{{ staff.cancelled_orders }}</td>
  </tr>
</template>

<script setup lang="ts">
import type { StaffStats } from "@api/types";

interface Props {
  staff: StaffStats;
}

interface Emits {
  (e: 'row-click', staff: StaffStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

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