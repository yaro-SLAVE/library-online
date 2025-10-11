import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from "@core/store/auth";
import type { Link } from "@core/types/types";

export function useStaffLinks() {
  const authStore = useAuthStore();
  const { isAuthenticated } = storeToRefs(authStore);

  const links = computed(() => {
    const rawLinks: Array<{ to: string; name: string; hide?: boolean }> = [
      {
        to: "/staff/profile",
        name: isAuthenticated.value ? "Профиль" : "Вход",
      },
      {
        to: "/staff/orders",
        name: "Заказы",
        hide: !isAuthenticated.value,
      },
      {
        to: "/staff/moderator",
        name: "Админка",
        hide: !isAuthenticated.value,
      },
    ];

    return rawLinks
      .filter((x) => !x.hide)
      .map((x): Link => ({ to: x.to, name: x.name }));
  });

  return { links };
}