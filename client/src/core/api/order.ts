//@ts-nocheck

import axios from "axios";
import type { BorrowedBook, Order, UserOrder, OrderStatusEnum, OrderCheckingInfo } from "./types";

export async function updateOrderStatus(
  orderId: number,
  newStatus: OrderStatusEnum,
  description?: string,
  books?: []
) {
  const statusUpdate = {
    description: description,
    status: newStatus,
  };

  try {
    const orderData = await getOrder(orderId);
    const currentOrder: Order = orderData;
    console.log(currentOrder);

    const updatedStatuses = [...currentOrder.statuses, statusUpdate];
    console.log(updatedStatuses);

    await axios.put(`/api/staff/order/${orderId}/`, { status: statusUpdate, books: books });
    console.log(`Статус заказа ${orderId} добавлен: "${newStatus}"`);
  } catch (error) {
    console.error("Ошибка при обновлении статуса заказа", error);
    throw error;
  }
}

export async function ordersList(): Promise<Order[]> {
  try {
    const { data } = await axios.get("/api/order/");
    console.log("/api/order/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка заказов", error);
    throw error;
  }
}

export async function fetchNewOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=new");
    console.log("Ответ сервера:", response);
    return response.data;
  } catch (error: unknown) {
    console.error(
      "Ошибка при получении новых заказов:",
      error instanceof Error ? error.message : String(error)
    );
    throw error;
  }
}

export async function fetchProcessingOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=processing");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении заказов в процессе:", error);
    throw error;
  }
}

export async function fetchReadyOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=ready");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении готовых заказов:", error);
    throw error;
  }
}

export async function fetchArchiveOrders(): Promise<UserOrder[]> {
  try {
    let data = [];
    const response = await axios.get("/api/staff/order/?status=done");
    data = response.data;
    const response2 = await axios.get("/api/staff/order/?status=cancelled");
    response2.data.forEach((element) => {
      data.push(element);
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении готовых заказов:", error);
    throw error;
  }
}

export async function getOrder(orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/staff/order/${orderId}/`);
    console.log(`/api/order/${orderId}`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении заказа", error);
    throw error;
  }
}

export async function checkOrder(orderId: number): Promise<OrderCheckingInfo> {
  try {
    const { data } = await axios.get(`/api/staff/order/check/${orderId}/`);
    console.log(`/api/order/${orderId}`, data);

    console.log("Найденные книги:", data.found_books);
    console.log("Ненайденные книги:", data.notfound_books);
    console.log("Аналоги:", data.additional_books);

    return data;
  } catch (error) {
    // if (error.response?.status === 404) {
    //   console.error('Заказ не найден');
    // } else if (error.response?.status === 401) {
    //   console.error('Требуется авторизация');
    // } else {
    //   console.error('Ошибка сервера');
    // }
    console.error("Ошибка при получении заказа", error);
    throw error;
  }
}

export async function getOrderStaff(orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/staff/order/${orderId}/`);
    console.log(`/api/staff/order/${orderId}`, data);

    if ((['ready', 'done', 'cancelled']).includes(data.statuses[data.statuses.length - 1].status)) {
      console.log('---------------------');
      let analogous_list = [...data.books].filter(x => x.analogous_order_item !== null).map(x => x.analogous_order_item);

      let done_books = [...data.books].filter(x => (x.status === 'ordered' || x.status === 'handed') && !analogous_list.includes(x.id)).map(x => {
        return {
          original: x,
          analogous: x
        }
      });

      let books_with_analogous = [...data.books]
      .filter(x => x.status === 'analogous')
      .map(x => {
        return {
          original: x,
          analogous: data.books.find(item => item.id === x.analogous_order_item)
        }
      });

      let cancelled_books = [...data.books].filter(x => x.status === 'cancelled').map(x => {
        return {
          original: x,
          analogous: null
        }
      });

      data.books = [...done_books, ...books_with_analogous, ...cancelled_books];
    }

    console.log(data);

    return data;
  } catch (error) {
    console.error("Ошибка при получении заказа", error);
    throw error;
  }
}

export async function createOrder(libraryId: number, bookIds: string[], borrowedBookIds: number[]) {
  try {
    await axios.post("/api/order/", {
      library: libraryId,
      books: bookIds,
      borrowed: borrowedBookIds,
    });
  } catch (error) {
    console.error("Ошибка при создании заказа", error);
    throw error;
  }
}

export async function editOrder(
  orderId: number,
  libraryId: number,
  bookIds: number[],
  borrowedBookIds: number[]
) {
  try {
    await axios.put(`/api/order/${orderId}/`, {
      library: libraryId,
      books: bookIds,
      borrowed: borrowedBookIds,
    });
  } catch (error) {
    console.error("Ошибка при редактировании заказа", error);
    throw error;
  }
}

export async function deleteOrder(orderId: number) {
  try {
    await axios.delete(`/api/order/${orderId}/`);
  } catch (error) {
    console.error("Ошибка при удалении заказа", error);
    throw error;
  }
}

export async function borrowedList(): Promise<BorrowedBook[]> {
  try {
    const { data } = await axios.get("/api/borrowed/");
    console.log("/api/borrowed/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка взятых книг", error);
    throw error;
  }
}
