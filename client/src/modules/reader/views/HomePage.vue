<template>
  <div class="container">
    <BooksSearch />

    <div class="announces">
      <div v-for="book in announces" :key="book.id" class="announce-book">
        <BookCard :book="book" :announcement="true" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import BookCard from "@reader/components/BookCard.vue";
import BooksSearch from "@reader/components/BooksSearch.vue";
import type { Book } from "@api/types";
import { announcesList } from "@api/announces";
const announces = ref<Book[]>([]);

onMounted(async () => {
  announces.value = await announcesList();
});
</script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

.container {
  padding-top: 20px;
}

.announces {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.announce-book {
  flex-basis: 90%;
  @include media-lg {
    flex-basis: 20%;
  }
}
</style>
