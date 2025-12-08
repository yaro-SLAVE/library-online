import {
  UsersIcon,
  ShoppingCartIcon,
  MinusCircleIcon,
  Cog6ToothIcon,
} from "@heroicons/vue/24/outline";

import type { SidebarLink } from "@core/types/types";

export const sidebarLinks: SidebarLink[] = [
  {
    name: "Читатели",
    to: "readers",
    icon: UsersIcon,
  },
  {
    name: "Заказы",
    to: "orders",
    icon: ShoppingCartIcon,
  },
  {
    name: "Сотрудники",
    to: "staff",
    icon: ShoppingCartIcon,
  },
  {
    name: "Черный список",
    to: "blacklist",
    icon: MinusCircleIcon,
  },
  {
    name: "Настройка системы",
    to: "settings",
    icon: Cog6ToothIcon,
  },
];
