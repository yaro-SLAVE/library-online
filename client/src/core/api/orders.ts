import axios from "axios";
import type { ModeratorOrderStats, ModeratorPaginatedOrders, ModeratorOrdersFilters, Order } from "./types";

export async function getModeratorOrders(filters?: ModeratorOrdersFilters): Promise<ModeratorOrdersFilters> {
  try {
    const { data } = await axios.get("/api/moderator/orders/", {
      params: {
        ...filters,
        ...(filters?.statuses && {
          'statuses[]': filters.statuses
        })
      },
      paramsSerializer: {
        indexes: null
      }
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка заказов", error);
    throw error;
  }
}

export async function getModeratorOrderDetail(orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/moderator/orders/${orderId}/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении деталей заказа ${orderId}`, error);
    throw error;
  }
}