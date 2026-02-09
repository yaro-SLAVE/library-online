import axios from "axios";
import type { StaffStats, PaginatedStaff, StaffFilters, Order, UserOrder } from "./types";

/**
 * Получить список сотрудников с фильтрацией
 */
export async function getStaff(filters?: StaffFilters): Promise<PaginatedStaff> {
  try {
    const { data } = await axios.get("/api/staff/", {
      params: filters,
      paramsSerializer: {
        indexes: null
      }
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка сотрудников", error);
    throw error;
  }
}

/**
 * Получить статистику по сотрудникам (с группировкой и агрегацией)
 */
export async function getStaffStats(filters?: StaffFilters): Promise<PaginatedStaff> {
  try {
    const { data } = await axios.get("/api/staff/stats/", {
      params: filters,
      paramsSerializer: {
        indexes: null
      }
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении статистики сотрудников", error);
    throw error;
  }
}

/**
 * Получить заказы сотрудника
 */
export async function getStaffOrders(staffId: number): Promise<UserOrder[]> {
  try {
    const { data } = await axios.get(`/api/staff/${staffId}/orders/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказов сотрудника ${staffId}`, error);
    throw error;
  }
}

/**
 * Получить детали заказа сотрудника
 */
export async function getStaffOrderDetail(staffId: number, orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/staff/${staffId}/orders/${orderId}/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказа ${orderId} сотрудника ${staffId}`, error);
    throw error;
  }
}

/**
 * Поиск сотрудников по ФИО или другим полям
 */
export async function searchStaff(query: string): Promise<StaffStats[]> {
  try {
    const { data } = await axios.get("/api/staff/search/", {
      params: { q: query }
    });
    return data;
  } catch (error) {
    console.error("Ошибка при поиске сотрудников", error);
    throw error;
  }
}