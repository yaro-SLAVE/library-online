<template>
  <div class="book-details">
    <div v-if="book.isbn?.[0]" class="book-row">
      <div class="icon-cell">🔢</div>
      <div class="content-cell">
        <span class="isbn">ISBN: {{ book.isbn[0] }}</span>
      </div>
    </div>

    <div class="book-row">
      <div class="icon-cell">📖</div>
      <div class="content-cell" @click="toggleExpand">
        <span class="book-title book">
          {{ displayedTitle }}
          <span v-if="!expanded && isTruncated">...</span>
          <span class="year"> ({{ book.year }}) </span>
        </span>
      </div>
    </div>

    <div v-if="book.author.length > 0 || book.collective.length > 0" class="book-row">
      <div class="icon-cell">
        <span v-if="book.author.length > 0">✍️</span>
        <span v-else-if="book.collective.length > 0">👥</span>
      </div>
      <div class="content-cell" @click="toggleExpandAuthor">
        <span class="author">
          {{ displayedAuthor }}
          <span v-if="!expandedAuthor && isTruncatedAuthor">...</span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { Book } from "../api/types";
const { book, truncate = false } = defineProps<{
  book: Book;
  truncate?: boolean;
}>();

const expanded = ref(false);
const expandedAuthor = ref(false);

const maxLength = 15;

const isTruncated = computed(() => truncate && book.title[0].length > maxLength);
const displayedTitle = computed(() => {
  if (!truncate) return book.title[0];
  return expanded.value ? book.title[0] : book.title[0].slice(0, maxLength);
});

const isTruncatedAuthor = computed(() => {
  const fullAuthor = book.author.length > 0 ? book.author.join(", ") : book.collective.join(", ");
  return truncate && fullAuthor.length > maxLength;
});
const displayedAuthor = computed(() => {
  const fullAuthor = book.author.length > 0 ? book.author.join(", ") : book.collective.join(", ");
  if (!truncate) return fullAuthor;
  return expandedAuthor.value ? fullAuthor : fullAuthor.slice(0, maxLength);
});

function toggleExpand() {
  if (truncate) expanded.value = !expanded.value;
}
function toggleExpandAuthor() {
  if (truncate) expandedAuthor.value = !expandedAuthor.value;
}
</script>

<style scoped lang="scss">
.book-details {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.book-row {
  display: flex;
  line-height: 1.3;
  justify-content: baseline;
}

.icon-cell {
  min-width: 1.5rem;
  text-align: center;
  padding-right: 0.3rem;
}

.content-cell {
  flex: 1;
  display: flex;
  align-items: flex-end;
  min-width: 0;
  cursor: pointer;
}

.book-title {
  font-size: 1.1rem;
  color: var(--color-text-700);
  display: inline;
}

.author {
  font-size: 0.95rem;
  color: var(--color-text-600);
  display: inline;
}

.year {
  font-size: 0.9rem;
  color: var(--color-text-600);
}

.isbn {
  font-size: 1.1rem;
  color: var(--color-text-600);
}
</style>
