import { useAuthStore } from "@core/store/auth";
import { storeToRefs } from "pinia";
import { watch } from "vue";

export function useAuthentication(hook: (isAuthenticated: boolean) => void) {
  const authStore = useAuthStore();
  const { isAuthenticated } = storeToRefs(authStore);

  watch(
    isAuthenticated,
    () => {
      hook(isAuthenticated.value);
    },
    {
      immediate: true,
    }
  );
}
