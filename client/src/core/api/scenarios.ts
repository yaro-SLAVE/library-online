import { api } from "./axios"
import type { Scenario } from "./types";

export async function scenariosList(): Promise<Scenario[]> {
  try {
    const { data } = await api.get("/api/scenario/");
    console.log("/api/scenario/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка сценариев поиска", error);
    throw error;
  }
}
