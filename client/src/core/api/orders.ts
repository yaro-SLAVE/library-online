// orders.ts (updated fullname mapping)
import axios from "axios";
import type { OrderStats, PaginatedOrderStats, OrdersFilters, Order, UserOrder, OrderStatusEnum } from "./types";
import { fetchNewOrders, fetchProcessingOrders, fetchReadyOrders, fetchArchiveOrders } from "./order";

export async function getOrdersStats(filters?: OrdersFilters): Promise<PaginatedOrderStats> {
  try {
    let newOrders = await fetchNewOrders();
    let processingOrders = await fetchProcessingOrders();
    let readyOrders = await fetchReadyOrders();
    let archiveOrders = await fetchArchiveOrders();

    const extractResults = (data: any): UserOrder[] => Array.isArray(data) ? data : data.results || [];

    newOrders = extractResults(newOrders);
    processingOrders = extractResults(processingOrders);
    readyOrders = extractResults(readyOrders);
    archiveOrders = extractResults(archiveOrders);

    let allOrders: UserOrder[] = [...newOrders, ...processingOrders, ...readyOrders, ...archiveOrders];

    // Apply filters client-side
    if (filters?.fullname) {
      allOrders = allOrders.filter(order => {
        const fullName = `${order.user.first_name || ''} ${order.user.last_name || ''}`.toLowerCase();
        return fullName.includes(filters.fullname?.toLowerCase() ?? '');
      });
    }
    if (filters?.statuses && filters.statuses.length > 0) {
      allOrders = allOrders.filter(order => {
        const lastStatus = order.statuses[order.statuses.length - 1]?.status;
        return filters.statuses?.includes(lastStatus as OrderStatusEnum) ?? false;
      });
    }
    if (filters?.date_from || filters?.date_to) {
      allOrders = allOrders.filter(order => {
        const lastStatus = order.statuses[order.statuses.length - 1];
        if (!lastStatus) return false;
        const date = new Date(lastStatus.date);
        if (filters.date_from && date < new Date(filters.date_from)) return false;
        if (filters.date_to && date > new Date(filters.date_to)) return false;
        return true;
      });
    }

    // Map to OrderStats
    const mappedResults: OrderStats[] = allOrders.map((uo: UserOrder): OrderStats => {
      const lastStatus = uo.statuses[uo.statuses.length - 1];
      let employee_collect = '';
      let employee_issue = '';
      for (const s of uo.statuses) {
        if (s.status === 'ready') {
          employee_collect = s.staff?.fullname ?? '';
        } else if (s.status === 'done') {
          employee_issue = s.staff?.fullname ?? '';
        }
      }
      return {
        id: uo.id,
        fullname: `${uo.user.first_name || ''} ${uo.user.last_name || ''}`.trim(),
        library_card: uo.user.library_card ?? null,
        employee_collect,
        employee_issue,
        status: lastStatus ? lastStatus.status : 'new' as OrderStatusEnum,
      };
    });

    // Apply remaining filters on mapped
    let filteredResults = mappedResults;
    if (filters?.employee_collect) {
      filteredResults = filteredResults.filter(stat => stat.employee_collect.toLowerCase().includes(filters.employee_collect?.toLowerCase() ?? ''));
    }
    if (filters?.employee_issue) {
      filteredResults = filteredResults.filter(stat => stat.employee_issue.toLowerCase().includes(filters.employee_issue?.toLowerCase() ?? ''));
    }

    // Sorting client-side
    if (filters?.sort_by) {
      filteredResults.sort((a, b) => {
        const key = filters.sort_by as keyof OrderStats;
        const valA = a[key] || '';
        const valB = b[key] || '';
        if (valA < valB) return filters.sort_order === 'asc' ? -1 : 1;
        if (valA > valB) return filters.sort_order === 'asc' ? 1 : -1;
        return 0;
      });
    }

    // Pagination client-side
    const page = filters?.page || 1;
    const page_size = filters?.page_size || 10;
    const start = (page - 1) * page_size;
    const paginatedResults = filteredResults.slice(start, start + page_size);

    return {
      count: filteredResults.length,
      next: null,
      previous: null,
      results: paginatedResults,
    };
  } catch (error) {
    console.error("Ошибка при получении списка заказов (stats)", error);
    throw error;
  }
}

export async function getOrderDetails(orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/staff/order/${orderId}/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении деталей заказа ${orderId}`, error);
    throw error;
  }
}