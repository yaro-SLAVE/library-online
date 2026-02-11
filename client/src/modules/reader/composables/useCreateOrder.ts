import { ref } from "vue";
import { useAuthStore } from "@core/store/auth";
import { useOrderStore } from "@reader/store/orderStore";
import { useBasketStore } from "@reader/store/basket";
import { useOrderProgress } from "./useOrderProgress";
import { storeToRefs } from "pinia";
import { ordersList, createOrder } from "@api/order";
import { getBook } from "@api/books";
import type { Order, OrderStatusEnum } from "@api/types";

export const useCreateOrder = () => {
  const authStore = useAuthStore();
  const { isAuthenticated } = storeToRefs(authStore);

  const orderStore = useOrderStore();
  const { selectedBooks, selectedBorrowedBooks, borrowedBooks } = storeToRefs(orderStore);

  const basketStore = useBasketStore();

  const { modalState, resetModalState } = useOrderProgress();

  const countOfBookInOrder = 5;
  const countOfBookPerPerson = 15;
  const userOrders = ref<Order[]>([]);

  const allowedStatusesToCountOrderedBooks: OrderStatusEnum[] = [
    "new",
    "processing",
    "ready",
    "done",
  ];

  const execute = async () => {
    resetModalState();
    modalState.value.isOpen = true;

    try {
      modalState.value.currentStep = 0;
      if (!isAuthenticated.value) failStep(modalState.value.currentStep);

      modalState.value.currentStep = 1;
      if (selectedBooks.value.length > countOfBookInOrder) failStep(modalState.value.currentStep);

      modalState.value.currentStep = 2;
      if (selectedBorrowedBooks.value.length < borrowedBooks.value.length)
        failStep(modalState.value.currentStep);

      modalState.value.currentStep = 3;
      userOrders.value = await ordersList();
      const canBeOrdered = await checkCanBeOrdered();
      if (!canBeOrdered) failStep(modalState.value.currentStep);

      modalState.value.currentStep = 4;
      const isValid = await validateOrder();
      if (!isValid) failStep(modalState.value.currentStep);

      modalState.value.currentStep = 5;
      const bookIds = selectedBooks.value.map((book) => book.id);
      await createOrder(selectedBooks.value[0].library, bookIds, selectedBorrowedBooks.value);
      try {
        await basketStore.clearOrderedBooks(bookIds);
      } catch {}

      orderStore.clearAll();
      await basketStore.updateBooks();

      modalState.value.isSuccess = true;
    } catch (error) {
      modalState.value.isError = true;
      throw error;
    }
  };

  const checkCanBeOrdered = async (): Promise<boolean> => {
    const checks = await Promise.all(
      selectedBooks.value.map(async (book) => {
        try {
          const fetchedBook = await getBook(book.id);
          return fetchedBook.can_be_ordered && !bookInOrders(book.id);
        } catch {
          return false;
        }
      })
    );

    selectedBooks.value = selectedBooks.value.filter((book, index) => {
      if (!checks[index]) {
        const message = `Книга:\n${book.brief}\nлибо будет удалена из заказа, она либо уже заказана, либо у вас на руках`;
        createMessage(message, modalState.value.currentStep);
      }
      return checks[index];
    });
    return checks.every(Boolean);
  };

  const bookInOrders = (targetBookId: string): boolean => {
    const isInOrders = userOrders.value.some((order) => {
      const lastStatus = order.statuses.at(-1);
      if (!lastStatus || !allowedStatusesToCountOrderedBooks.includes(lastStatus.status)) {
        return false;
      }
      return order.books.some((bookItem) => bookItem.book.id === targetBookId);
    });

    const isInBorrowed = borrowedBooks.value.some(
      (borrowedBook) => borrowedBook.book.id === targetBookId
    );

    return isInOrders || isInBorrowed;
  };

  const validateOrder = async (): Promise<boolean> => {
    const librarySet = new Set(selectedBooks.value.map((book) => book.library));
    const orderedBooksCount = booksOrdered();
    const totalItems =
      borrowedBooks.value.length -
      selectedBorrowedBooks.value.length +
      selectedBooks.value.length +
      orderedBooksCount;
    return totalItems > 0 && totalItems <= countOfBookPerPerson && librarySet.size === 1;
  };

  const booksOrdered = (): number => {
    const countOfBooksPreviousOrders = userOrders.value.reduce((total, order) => {
      const lastStatus = order.statuses[order.statuses.length - 1];
      if (lastStatus && allowedStatusesToCountOrderedBooks.includes(lastStatus.status)) {
        const validBooks = order.books.filter((book) => book.status === "ordered");

        return total + validBooks.length;
      }
      return total;
    }, 0);
    return countOfBooksPreviousOrders;
  };

  const failStep = (stepIndex: number) => {
    modalState.value.currentStep = stepIndex;
    modalState.value.isError = true;
    throw Error;
  };

  const createMessage = (msg: string, stepIndex: number) => {
    modalState.value.steps[stepIndex].messages ??= [];
    modalState.value.steps[stepIndex].messages.push(msg);
  };

  return {
    execute,
    modalState,
  };
};
