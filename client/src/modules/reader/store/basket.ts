import {
  addBasketBook,
  addBasketBooks,
  deleteBasketBook,
  basketBooksList,
  replaceBasketBooks,
} from "@api/basket";
import type { Book } from "@api/types";
import { useAuthentication } from "@core/composables/auth";
import { useLocalStorage } from "@vueuse/core";
import { defineStore, storeToRefs } from "pinia";
import { ref } from "vue";
import { useToast } from "vue-toastification";
import { useAuthStore } from "@core/store/auth";

export const useBasketStore = defineStore("basket", () => {
  const toast = useToast();
  const authStore = useAuthStore();

  const { isAuthenticated } = storeToRefs(authStore);
  const localBooks = useLocalStorage<Book[]>("basketBooks", []);
  const books = ref<Book[]>([]);

  async function updateBooks() {
    if (isAuthenticated.value) {
      books.value = await basketBooksList();
    } else {
      books.value = localBooks.value;
    }
  }

  async function addBook(book: Book) {
    if (isAuthenticated.value) {
      await addBasketBook(book.id);
    } else {
      if (localBooks.value.filter((b) => b.id === book.id).length === 0) {
        localBooks.value.push(book);
      }
    }

    let shortTitle: string = "Книга";
    const limit = 60;
    if (book.title[0].length <= limit) {
      shortTitle = book.title[0].substring(0, limit);
    } else {
      shortTitle = `${book.title[0].substring(0, limit - 3)}...`;
    }

    toast.success(shortTitle + " добавленa в корзину");

    await updateBooks();
  }

  async function removeBook(book: Book) {
    if (isAuthenticated.value) {
      await deleteBasketBook(book.id);
    } else {
      localBooks.value = localBooks.value.filter((b) => b.id !== book.id);
    }
    await updateBooks();
  }

  async function clearBooks() {
    if (isAuthenticated.value) {
      await replaceBasketBooks([]);
    } else {
      localBooks.value = [];
    }
    await updateBooks();
  }

  async function clearOrderedBooks(selectedIds: string[]) {
    for (const id of selectedIds) {
      console.log(id);
      await deleteBasketBook(id).catch(() => console.log("Ошибка при удалении элемента корзины"));
    }
  }

  useAuthentication(async (auth) => {
    if (auth) {
      await addBasketBooks(localBooks.value.map((book) => book.id));
      localBooks.value = [];
    }

    await updateBooks();
  });

  return {
    books,
    updateBooks,
    addBook,
    removeBook,
    clearBooks,
    clearOrderedBooks,
  };
});
