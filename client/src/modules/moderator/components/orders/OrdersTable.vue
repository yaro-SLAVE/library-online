<template>
  <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <SortableHeader
            field="id"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            ID
          </SortableHeader>

          <SortableHeader
            field="fullname"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Читатель
          </SortableHeader>

          <th class="static-header">
            Чит.билет
          </th>

          <SortableHeader
            field="library"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Библиотека
          </SortableHeader>

          <SortableHeader
            field="status"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Статус
          </SortableHeader>

          <SortableHeader
            field="books_count"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Книг
          </SortableHeader>

          <SortableHeader
            field="employee_collect"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Собрал
          </SortableHeader>

          <SortableHeader
            field="employee_issue"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Выдал
          </SortableHeader>

          <SortableHeader
            field="created_date"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Дата создания
          </SortableHeader>
        </tr>
      </thead>
      <tbody>
        <OrdersTableRow 
          v-for="order in ordersData" 
          :key="order.id" 
          :order="order" 
          @row-click="$emit('row-click', $event)"
        />
      </tbody>
    </table>

    <Pagination
      v-if="ordersData.length > 0"
      :current-page="pagination.page"
      :total-pages="totalPages"
      :loading="loading"
      @prev="prevPage"
      @next="nextPage"
    />

    <OrdersEmptyState
      v-if="ordersData.length === 0 && !loading"
      :has-active-filters="hasActiveFilters"
      @clear-filters="$emit('clear-filters')"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import OrdersTableRow from "@moderator/components/orders/OrdersTableRow.vue";
import SortableHeader from '@modules/moderator/components/SortableHeader.vue';
import Pagination from '@modules/moderator/components/Pagination.vue';
import OrdersEmptyState from '@moderator/components/orders/OrdersEmptyState.vue';
import type { ModeratorOrderStats } from "@api/types";
import { computed } from 'vue';

interface Props {
  ordersData: ModeratorOrderStats[];
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
  (e: 'row-click', order: ModeratorOrderStats): void;
}

const props = withDefaults(defineProps<Props>(), {
  ordersData: () => []
});
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
  
  th, td {
    white-space: nowrap;
  }
}

th {
  padding: 12px;
  text-align: left;
  color: var(--color-text-800);
  background-color: var(--color-background-100);
  vertical-align: middle;
}

.static-header {
  cursor: default;
  width: 120px;
  min-width: 120px;
  max-width: 120px;
  
  &:hover {
    background-color: var(--color-background-100);
  }
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}
</style>