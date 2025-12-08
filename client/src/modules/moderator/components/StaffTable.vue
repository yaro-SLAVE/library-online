<template>
  <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <SortableHeader
            field="fullname"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            ФИО сотрудника
          </SortableHeader>

          <SortableHeader
            field="department"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Подразделение
          </SortableHeader>

          <SortableHeader
            field="total_orders"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Количество заказов
          </SortableHeader>

          <SortableHeader
            field="cancelled_orders"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Количество отказов
          </SortableHeader>
        </tr>
      </thead>
      <tbody>
        <StaffTableRow 
          v-for="staff in staffData" 
          :key="staff.id" 
          :staff="staff" 
          @row-click="$emit('row-click', $event)"
        />
      </tbody>
    </table>

    <Pagination
      v-if="staffData.length > 0"
      :current-page="pagination.page"
      :total-pages="totalPages"
      :loading="loading"
      @prev="prevPage"
      @next="nextPage"
    />

    <EmptyState
      v-if="staffData.length === 0 && !loading"
      :has-active-filters="hasActiveFilters"
      @clear-filters="$emit('clear-filters')"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import SortableHeader from '@moderator/components/SortableHeader.vue';
import Pagination from '@moderator/components/Pagination.vue';
import EmptyState from '@moderator/components/EmptyState.vue';
import StaffTableRow from '@moderator/components/StaffTableRow.vue';
import type { StaffStats } from "@api/types";
import { computed } from 'vue';

interface Props {
  staffData: StaffStats[];
  loading: boolean;
  sortField: string;
  sortDirection: 'asc' | 'desc';
  pagination: {
    page: number;
    total: number;
    limit: number;
  };
  hasActiveFilters: boolean;
}

interface Emits {
  (e: 'sort', field: string, direction: 'asc' | 'desc'): void;
  (e: 'prev-page'): void;
  (e: 'next-page'): void;
  (e: 'clear-filters'): void;
  (e: 'row-click', staff: StaffStats): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const totalPages = computed(() => 
  Math.ceil(props.pagination.total / props.pagination.limit)
);

const onSort = (field: string, direction: 'asc' | 'desc') => {
  emit('sort', field, direction);
};

const prevPage = () => {
  emit('prev-page');
};

const nextPage = () => {
  emit('next-page');
};
</script>

<style scoped lang="scss">
.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

th {
  padding: 12px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
  vertical-align: middle;
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}
</style>