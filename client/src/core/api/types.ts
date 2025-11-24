export const groups = {
  Reader: "Читатель",
  Librarian: "Библиотекарь",
} as const;
export type Group = keyof typeof groups;

export type ProfileInfo = {
  username: string;
  first_name: string;
  last_name: string;
  groups: Group[];
  fullname: string;
  department: string;
};

export type Library = {
  id: number;
  description: string;
  address: string;
};

export type Scenario = {
  prefix: string;
  description: string | null;
};

export type BookLink = {
  url: string;
  description: string | null;
};

export type Book = {
  id: string;
  library: number;
  description: string;
  year: number;
  copies: number;
  can_be_ordered: boolean;
  links: BookLink[];
  author: string[];
  collective: string[];
  title: string[];
  isbn: string[];
  language: string[];
  country: string[];
  city: string[];
  publisher: string[];
  subject: string[];
  keyword: string[];
  cover: string | null;
  brief: string | null;
  created: string | null;
};

export const orderStatuses = {
  new: "Новый",
  processing: "Собирается",
  ready: "Готов к выдаче",
  done: "Выполнен",
  cancelled: "Отменен",
  error: "Ошибка",
  archived: "Заархивирован",
} as const;
export type OrderStatusEnum = keyof typeof orderStatuses;

export type OrderStatus = {
  status: OrderStatusEnum;
  date: string;
  description: string;
  staff: ProfileInfo;
};

export const orderBookStatuses = {
  ordered: "Заказана",
  handed: "Выдана",
  returned: "Возвращена",
  cancelled: "Заказ отменен",
} as const;
export type OrderBookStatus = keyof typeof orderBookStatuses;

export type OrderBook = {
  id: number;
  book: Book;
  status: OrderBookStatus;
  handed_date: string | null;
  to_return_date: string | null;
  returned_date: string | null;
};

export type Order = {
  id: number;
  books: OrderBook[];
  statuses: OrderStatus[];
  library: Library;
  user: UserInfo;
};

export type BorrowedBook = {
  id: number;
  book: Book;
  order: number;
  handed_date: string;
  to_return_date: string;
};

export type UserOrder = {
  id: number;
  statuses: OrderStatus[];
  library: Library;
  user: UserInfo;
};

export type UserInfo = {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  library_card: string | null;
  campus_id: string | null;
  mira_id: string | null;
  fullname: string;
  department: string;
};

export type PaginatedOrders = {
  count: number;
  next: string | null;
  previous: string | null;
  results: UserOrder[];
};

export type OrderCheckingInfo = {
  found_books: OrderBook[];
  notfound_books: OrderBook[];
  additional_books: string[];
};

export type ReaderStats = {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  fullname: string;
  department: string;
  library_card: string | null;
  campus_id: string | null;
  mira_id: string | null;
  total_books_ordered: number;
  total_orders: number;
  cancelled_orders: number;
  last_order_date: string | null;
};

export type PaginatedReaders = {
  count: number;
  next: string | null;
  previous: string | null;
  results: ReaderStats[];
};

export type ReadersFilters = {
  fullname?: string;
  department?: string;
  last_order_date_from?: string;
  last_order_date_to?: string;
  current_order_statuses?: OrderStatusEnum[];
  sort_by?: 'id' | 'fullname' | 'department' | 'total_books_ordered' | 'total_orders' | 'cancelled_orders';
  sort_order?: 'asc' | 'desc';
  page?: number;
  page_size?: number;
};