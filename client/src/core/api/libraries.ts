import axios from "axios";
import type { Library } from "./types";

export async function librariesList(): Promise<Library[]> {
  try {
    const { data } = await axios.get("/api/library/");
    console.log("/api/library/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка библиотек", error);
    throw error;
  }
}
