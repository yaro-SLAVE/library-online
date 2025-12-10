<template>
  <ModalDialog v-model="visible">
    <div class="dialog">
      <h3>Подробнее о книге</h3>

      <div class="body">
        <div class="book-image">
          <BookImage :book="book" />
        </div>

        <div>
          <h5 v-for="[index, title] in book.title.entries()" v-bind:key="index" class="title">
            {{ title }}
          </h5>
          <p class="text-muted">Год: {{ book.year }}</p>

          <p v-if="book.author.length > 0" class="text-muted">
            Авторы: {{ book.author.join(", ") }}
          </p>
          <p v-else-if="book.collective.length > 0" class="text-muted">
            Коллективы: {{ book.collective.join(", ") }}
          </p>

          <p>Количество: {{ book.copies }}</p>

          <p>{{ book.description }}</p>

          <p>
            Ссылки:
            <a v-for="[index, link] in book.links.entries()" v-bind:key="index" :href="link.url">
              {{ link.description }}
            </a>
          </p>

          <StyledButton @click="basketStore.addBook(book)" :disabled="isInBasket">
            <ShoppingCartIcon class="cart-icon" />В корзину
          </StyledButton>
          <h6 class="text-muted">{{ book.keyword.join(", ") }}</h6>
        </div>
      </div>

      <div class="text-end">
        <StyledButton theme="accent" @click="visible = false">Закрыть</StyledButton>
      </div>
    </div>
  </ModalDialog>
</template>

<script setup lang="ts">
import type { Book } from "@api/types";
import { useBasketStore } from "@reader/store/basket";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import { ShoppingCartIcon } from "@heroicons/vue/24/outline";
import StyledButton from "@components/StyledButton.vue";
import BookImage from "@reader/components/BookImage.vue";
import ModalDialog from "@components/ModalDialog.vue";

const { book } = defineProps<{
  book: Book;
}>();

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.id));

const visible = defineModel<boolean>({ required: true });
</script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

.dialog {
  width: 90vw;

  @include media-lg {
    max-width: 1000px;
    width: auto;
  }
}

.body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;

  @include media-lg {
    flex-direction: row;
    align-items: start;
  }
}

.title {
  margin-top: 0rem;
  margin-bottom: 0rem;
}

.text-muted {
  color: var(--color-text-400);
}

.cart-icon {
  width: 1.2em;
  height: 1.2em;
  margin-right: 0.5em;
}

.book-image {
  flex-shrink: 0;
  flex-grow: 0;
  flex-basis: 200px;

  width: 50%;
  height: auto;

  @include media-lg {
    width: auto;
    height: 290px;
  }
}
</style>
