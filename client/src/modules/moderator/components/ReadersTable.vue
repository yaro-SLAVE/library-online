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
            field="department"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Подразделение
          </SortableHeader>

          <SortableHeader
            field="total_books_ordered"
            :current-field="sortField"
            :direction="sortDirection"
            :loading="loading"
            @sort="onSort"
          >
            Количество заказанных книг
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
            Количество отмененных заказов
          </SortableHeader>
        </tr>
      </thead>
      <tbody>
        <ReadersTableRow 
          v-for="reader in readersData" 
          :key="reader.id" 
          :reader="reader" 
          @row-click="$emit('row-click', $event)"
        />
      </tbody>
    </table>

    <Pagination
      v-if="readersData.length > 0"
      :current-page="pagination.page"
      :total-pages="totalPages"
      :loading="loading"
      @prev="prevPage"
      @next="nextPage"
    />

    <EmptyState
      v-if="readersData.length === 0 && !loading"
      :has-active-filters="hasActiveFilters"
      @clear-filters="$emit('clear-filters')"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import ReadersTableRow from "@modules/moderator/components/ReadersTableRow.vue";
import SortableHeader from '@modules/moderator/components/SortableHeader.vue';
import Pagination from '@modules/moderator/components/Pagination.vue';
import EmptyState from '@modules/moderator/components/EmptyState.vue';
import type { ReaderStats } from "@api/types";
import { computed } from 'vue';

interface Props {
  readersData: ReaderStats[];
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
  (e: 'row-click', reader: ReaderStats): void;
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