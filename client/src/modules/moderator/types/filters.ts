import type { OrderStatusEnum } from "@api/types";

export type ModeratorFiltersModel = {
  fullname: string;
  department: string;
  lastOrderDateFrom: string;
  lastOrderDateTo: string;
  currentOrderStatuses: OrderStatusEnum[];
  employee_collect?: string;
  employee_issue?: string;
};
