<template>
  <div class="card" :class="{ announcement: announcement }" :title="bookHint">
    <div class="book-image" :class="{ announcement: announcement }">
      <BookImage class="book-image-inner" :class="{ announcement: announcement }" :book="book" />
    </div>

    <div class="card-body">
      <h5 class="card-title">{{ book.title[0] }}</h5>
      <h5 class="card-year">{{ book.year }} г.</h5>
      <h6 v-if="book.author.length > 0" class="card-subtitle">
        {{ book.author.join(", ") }}
      </h6>
      <h6 v-else-if="book.collective.length > 0" class="card-subtitle">
        {{ book.collective.join(", ") }}
      </h6>
      <h6 class="card-subtitle">
        {{ book.brief }}
      </h6>

      <div class="buttons">
        <StyledButton
          v-if="!basketCart"
          theme="primary"
          @click="addBook"
          :disabled="isAdding || isInBasket"
          class="button"
          :class="{ announcement: announcement }"
        >
          В Корзину <ShoppingCartIcon class="button-icon" />
        </StyledButton>

        <StyledButton
          theme="secondary"
          type="button"
          @click="isModalVisible = true"
          class="button"
          :class="{ announcement: announcement }"
        >
          Подробнее <Bars3Icon class="button-icon" />
        </StyledButton>

        <a
          v-if="bookLink !== undefined"
          :href="bookLink"
          class="button"
          :class="{ announcement: announcement }"
        >
          <StyledButton theme="accent" class="w-full">
            Читать онлайн <BookOpenIcon class="button-icon" />
          </StyledButton>
        </a>

        <StyledButton
          v-if="basketCart"
          theme="accent"
          @click="basketStore.removeBook(book)"
          class="button"
          :class="{ announcement: announcement }"
        >
          Удалить <TrashIcon class="button-icon" />
        </StyledButton>
      </div>
    </div>
  </div>

  <AboutBookDialog :book="book" v-model="isModalVisible" />
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { Book } from "@api/types";
import { ShoppingCartIcon, Bars3Icon, BookOpenIcon, TrashIcon } from "@heroicons/vue/24/outline";
import { useBasketStore } from "@reader/store/basket";
import { storeToRefs } from "pinia";
import AboutBookDialog from "@reader/components/AboutBookDialog.vue";
import StyledButton from "@components/StyledButton.vue";
import BookImage from "@reader/components/BookImage.vue";

const {
  book,
  announcement = false,
  basketCart = false,
} = defineProps<{
  book: Book;
  announcement?: boolean;
  basketCart?: boolean;
}>();

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.id));

const isModalVisible = ref(false);
const isAdding = ref(false);

async function addBook() {
  if (isInBasket.value || isAdding.value) return;
  isAdding.value = true;

  await basketStore
    .addBook(book)
    .catch((error) => {
      console.error("Ошибка при добавлении книги:", error);
    })
    .finally(() => {
      if (!isInBasket.value) isAdding.value = false;
    });
}

const bookLink = computed(
  () => book.links.filter((link) => link.description === "Электронная библиотека ИРНИТУ")[0]?.url
);

const bookHint = computed(() => {
  if (book.can_be_ordered) {
    if (book.copies > 0) {
      return `Книга доступна для заказа \nКниг, доступных для заказа: ${book.copies}`;
    } else {
      return "Доступных книг для заказа пока нет, закажите позже или возьмите в читальном зале";
    }
  } else {
    if (book.links.length > 0) {
      return "Можете только прочитать книгу онлайн";
    } else {
      return "Книга доступна только в зале";
    }
  }
});
</script>

<style scoped lang="scss">
@use "@assets/styles/breakpoints.scss" as *;

@mixin vertical-layout {
  &.announcement {
    @content;
  }

  @include media-max-lg {
    @content;
  }
}

.card {
  width: 100%;

  background-color: var(--color-background-50);
  border-style: solid;
  border-radius: 0.5rem;
  border-width: 1px;
  border-color: var(--color-text-300);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: row;

  @include vertical-layout {
    flex-direction: column;
    min-width: 400px;
  }
}

.card-body {
  padding: 1rem 0.5rem 1rem 0.5rem;
}

.card-title {
  font-size: var(--text-lg);
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-year {
  font-size: var(--text-md);
  font-weight: bold;
}

.card-subtitle {
  color: var(--color-text-700);
  margin-bottom: 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-image {
  flex-shrink: 0;
  flex-grow: 0;
  flex-basis: 190px;

  @include vertical-layout {
    height: 290px;
    flex-basis: 200px;
    transition: all 0.2s;

    &:hover {
      height: 600px;
    }
  }
}

.book-image-inner {
  border-top-left-radius: 0.5rem;
  border-bottom-left-radius: 0.5rem;

  @include vertical-layout {
    border-top-right-radius: 0.5rem;
    border-bottom-left-radius: 0rem;
  }
}

.buttons {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 1rem;
}

.button {
  @include vertical-layout {
    flex-grow: 1;
  }
}

.button-icon {
  width: 1.2em;
  height: 1.2em;
  margin-left: 0.5em;
}
</style>
