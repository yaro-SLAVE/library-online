import type { Book } from "./types";
import { api } from "./axios"

export async function announcesList(): Promise<Book[]> {
  try {
    const { data } = await api.get("/api/book/announcement/");
    console.log("/api/book/announcement/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при поиске новинок", error);
    throw error;
  }
}
