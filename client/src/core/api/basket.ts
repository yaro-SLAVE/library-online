import axios from "axios";
import type { Book } from "./types";

export async function basketBooksList(): Promise<Book[]> {
  try {
    const { data } = await axios.get("/api/basket/");
    console.log("/api/basket/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка книг в корзине", error);
    throw error;
  }
}

export async function addBasketBooks(bookIds: string[]) {
  try {
    await axios.post("/api/basket/", {
      books: bookIds,
    });
  } catch (error) {
    console.error("Ошибка при добавлении книг в корзину", error);
    throw error;
  }
}

export async function addBasketBook(bookId: string) {
  await addBasketBooks([bookId]);
}

export async function replaceBasketBooks(bookIds: string[]) {
  try {
    await axios.put("/api/basket/replace/", {
      books: bookIds,
    });
  } catch (error) {
    console.error("Ошибка при изменении книг в корзине", error);
    throw error;
  }
}

export async function deleteBasketBook(bookId: string) {
  try {
    await axios.delete(`/api/basket/${bookId}/`);
  } catch (error) {
    console.error("Ошибка при удалении книги из корзины", error);
    throw error;
  }
}
