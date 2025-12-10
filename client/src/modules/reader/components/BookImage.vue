<template>
  <img v-if="book.cover !== null" :src="book.cover" />

  <div v-else class="book-fake-image">
    <span>{{ book.title[0] }}</span>
    <div v-if="book.author.length > 0">
      <div v-if="book.author.length <= 2">
        <span>{{ book.author.join(", ") }}</span>
      </div>
      <div v-else>
        <span>{{ book.author.slice(0, 2).join(", ") }} и другие</span>
      </div>
    </div>
    <span v-else-if="book.collective.length > 0">{{ book.collective.join(", ") }}</span>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@api/types";

const { book } = defineProps<{
  book: Book;
}>();
</script>

<style scoped lang="scss">
@use "@assets/styles/colors.scss" as *;

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-fake-image {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;

  text-align: center;
  justify-content: center;
  align-items: center;

  padding: 0.25rem;

  background-color: var(--color-background-200);
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  font-size: var(--text-xs);

  span {
    margin-bottom: 2em;
  }

  @include light-theme {
    color: var(--color-text-50);
  }

  @include dark-theme {
    color: var(--color-text-950);
  }
}
</style>
