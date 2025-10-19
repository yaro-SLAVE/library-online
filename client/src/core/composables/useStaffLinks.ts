import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@core/store/auth";
import type { Link } from "@core/types/types";
import { useUserStore } from "@core/store/user";

export const useStaffLinks = () => {
  const authStore = useAuthStore();
  const userStore = useUserStore();
  const { isAuthenticated } = storeToRefs(authStore);
  const { currentRole } = storeToRefs(userStore);
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
        to: "/moderator",
        name: "Админка",
        hide: currentRole.value !== "Admin",
      },
    ];

    return rawLinks.filter((x) => !x.hide).map((x): Link => ({ to: x.to, name: x.name }));
  });

  return { links };
};
