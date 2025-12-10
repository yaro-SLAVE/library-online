import axios from "axios";
import type { Book } from "./types";

export async function announcesList(): Promise<Book[]> {
  try {
    const { data } = await axios.get("/api/book/announcement/");
    console.log("/api/book/announcement/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при поиске новинок", error);
    throw error;
  }
}
