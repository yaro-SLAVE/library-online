import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from "@core/store/auth";
import type { Link } from "@core/types/types";

export const useReaderLinks = () => {
  const authStore = useAuthStore();
  const { isAuthenticated } = storeToRefs(authStore);

  const links = computed(() => {
    const rawLinks: Array<{ to: string; name: string; hide?: boolean }> = [
      {
        to: "/profile",
        name: isAuthenticated.value ? "Профиль" : "Вход",
      },
      {
        to: "/basket",
        name: "Корзина",
      },
      {
        to: "/orders",
        name: "Заказы",
        hide: !isAuthenticated.value, 
      },
      {
        to: "/note",
        name: "О проекте",
      },
    ];

    return rawLinks
      .filter((x) => !x.hide)
      .map((x): Link => ({ to: x.to, name: x.name }));
  });

  return { links };
}