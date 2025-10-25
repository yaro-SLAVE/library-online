import axios from "axios";
import type { LiveStats } from "./types";

export async function liveStats(): Promise<LiveStats> {
  try {
    const { data } = await axios.get("/api/stats/live");
    console.log("/api/stats/live", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении текущей статистики", error);
    throw error;
  }
}
