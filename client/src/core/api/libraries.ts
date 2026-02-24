import type { Library } from "./types";
import { api } from "./axios"

export async function librariesList(): Promise<Library[]> {
  try {
    const { data } = await api.get("/api/library/");
    console.log("/api/library/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка библиотек", error);
    throw error;
  }
}
