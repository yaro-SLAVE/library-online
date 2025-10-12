import { computed } from "vue";
import type { Link } from "@core/types/types";

export const useModeratorLinks = () => {
  const links = computed(() => {
    const rawLinks: Array<{ to: string; name: string; hide?: boolean }> = [
      {
        to: "/staff/orders",
        name: "К заказам",
      },
    ];

    return rawLinks.filter((x) => !x.hide).map((x): Link => ({ to: x.to, name: x.name }));
  });

  return { links };
};
