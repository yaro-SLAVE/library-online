// api/readers.ts
import axios from "axios";
import type { ReaderStats, PaginatedReaders, ReadersFilters } from "./types";

export async function getReaders(filters?: ReadersFilters): Promise<PaginatedReaders> {
  try {
    const { data } = await axios.get("/api/readers/", {
      params: {
        ...filters,
        // Преобразуем массивы в формат, который понимает Django
        ...(filters?.current_order_statuses && {
          'current_order_statuses[]': filters.current_order_statuses
        })
      },
      paramsSerializer: {
        indexes: null // Отключаем индексацию для массивов
      }
    });
    console.log("/api/readers/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка читателей", error);
    throw error;
  }
}

export async function getReaderDetails(readerId: number): Promise<ReaderStats> {
  try {
    const { data } = await axios.get(`/api/readers/${readerId}/details/`);
    console.log(`/api/readers/${readerId}/details/`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении детальной информации о читателе", error);
    throw error;
  }
}

export async function getReaderOrders(readerId: number): Promise<any> {
  try {
    const { data } = await axios.get(`/api/readers/${readerId}/orders/`);
    console.log(`/api/readers/${readerId}/orders/`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении заказов читателя", error);
    throw error;
  }
}