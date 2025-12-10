import axios from "axios";
import type { Book } from "./types";

export async function searchBooks(expression: string, library?: number): Promise<Book[]> {
  try {
    const { data } = await axios.get("/api/book/", {
      params: {
        expression: expression,
        library: library,
      },
    });
    console.log("/api/book/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка книг", error);
    throw error;
  }
}

export async function getBook(bookId: string): Promise<Book> {
  try {
    const { data } = await axios.get(`/api/book/${bookId}`);
    console.log(`/api/book/${bookId}`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении книги по айди", error);
    throw error;
  }
}
