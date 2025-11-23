import axios from "axios";
import type { ReaderStats, PaginatedReaders, ReadersFilters, Order, UserOrder } from "./types";

export async function getReaders(filters?: ReadersFilters): Promise<PaginatedReaders> {
  try {
    const { data } = await axios.get("/api/readers/", {
      params: {
        ...filters,
        ...(filters?.current_order_statuses && {
          'current_order_statuses[]': filters.current_order_statuses
        })
      },
      paramsSerializer: {
        indexes: null
      }
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка читателей", error);
    throw error;
  }
}

export async function getReaderOrders(readerId: number): Promise<UserOrder[]> {
  try {
    const { data } = await axios.get(`/api/readers/${readerId}/orders/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказов читателя ${readerId}`, error);
    throw error;
  }
}

export async function getReaderOrderDetail(readerId: number, orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/readers/${readerId}/orders/${orderId}/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказа ${orderId} читателя ${readerId}`, error);
    throw error;
  }
}