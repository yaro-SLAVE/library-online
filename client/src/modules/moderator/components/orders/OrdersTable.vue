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
            #
          </SortableHeader>

          <SortableHeader
            field="fullname"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            ФИО читателя
          </SortableHeader>

          <SortableHeader
            field="employee_collect"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Сотрудник собрал
          </SortableHeader>

          <SortableHeader
            field="employee_issue"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Сотрудник выдал
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

    <EmptyState
      v-if="ordersData.length === 0 && !loading"
      :has-active-filters="hasActiveFilters"
      @clear-filters="$emit('clear-filters')"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import OrdersTableRow from "../orders/OrdersTableRow.vue";
import SortableHeader from '@modules/moderator/components/SortableHeader.vue';
import Pagination from '@modules/moderator/components/Pagination.vue';
import EmptyState from '@modules/moderator/components/EmptyState.vue';
import type { OrderStats } from "@api/types";
import { computed } from 'vue';

interface Props {
  ordersData: OrderStats[];
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
  (e: 'row-click', order: OrderStats): void;
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
}

tr {
  border-bottom: 1px solid var(--color-text-200);
}
</style>

