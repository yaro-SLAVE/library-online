<template>
  <div class="borrow-summary">
    <div class="summary-header">
      <span class="alert-icon">⚠️</span>
      <h3 class="summary-title">
        Книги, которые у вас на руках. <br />Подтвердите, что принесете их. <br />
      </h3>
    </div>

    <div class="book-list">
      <div v-for="item in orderStore.borrowedBooks" :key="item.book.id" class="book-item card">
        <div class="book-activities">
          <label class="book-content">
            <StyledCheckbox :value="item.id" v-model="orderStore.selectedBorrowedBooks" />
            <ShortBookCard :book="item.book" />
          </label>
          <div class="in-depth" v-if="inDebt(item.to_return_date)">
            <div class="in-depth-info">Задолженность</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useOrderStore } from "@reader/store/orderStore";
import ShortBookCard from "@components/ShortBookCard.vue";
import StyledCheckbox from "@components/StyledCheckbox.vue";
const orderStore = useOrderStore();

const inDebt = (bookOnReturnDate: string): boolean => {
  const today = new Date().toLocaleDateString();
  const bookOnReturn = new Date(bookOnReturnDate).toLocaleDateString();
  return bookOnReturn >= today;
};
</script>

<style scoped lang="scss">
.in-depth-info {
  color: var(--color-accent-600);
  padding: 0.5rem;
  border-radius: 1rem;
}

.in-depth-info:hover {
  cursor: help;
}

.in-depth {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.book-activities {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.borrow-summary {
  background: var(--color-background-100);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
}

.alert-icon {
  font-size: 1.8rem;
}

.summary-title {
  margin: 0;
  color: var(--color-accent-500);
  font-size: 1.4rem;
}

.book-list {
  display: grid;
  gap: 1rem;
}

.book-item {
  padding: 1rem;
  transition: all 0.2s ease;
}

.book-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  cursor: pointer;
}
</style>
