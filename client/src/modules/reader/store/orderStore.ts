import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { ref } from "vue";

import { deleteOrder, borrowedList } from "@api/order";
import type { Book, Order, BorrowedBook } from "@api/types";

export const useOrderStore = defineStore("orderStore", () => {
  const selectedBooks = useLocalStorage<Book[]>("selectedBooksToOrder", []);
  const selectedBorrowedBooks = ref<number[]>([]);
  const borrowedBooks = ref<BorrowedBook[]>([]);
  const userOrders = ref<Order[]>([]);

  const handleDeleteOrder = async (orderId: number) => {
    try {
      await deleteOrder(orderId);
    } catch (error) {
      console.log(error);
    }
  };

  const getBorrowedBooks = async () => {
    borrowedBooks.value = await borrowedList();
  };

  const removeSelectedBook = (id: string) => {
    selectedBooks.value = selectedBooks.value.filter((book) => book.id !== id);
  };

  const addBook = (newBook: Book) => {
    selectedBooks.value.push(newBook);
  };

  const clearAll = () => {
    selectedBooks.value = [];
    selectedBorrowedBooks.value = [];
    borrowedBooks.value = [];
    userOrders.value = [];
  };

  return {
    selectedBooks,
    selectedBorrowedBooks,
    borrowedBooks,
    handleDeleteOrder,
    addBook,
    clearAll,
    getBorrowedBooks,
    removeSelectedBook,
  };
});
