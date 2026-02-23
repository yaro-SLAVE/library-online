import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { useAuthStore } from "./auth";
import { profileInfo, setRole } from "@api/profile";
import type { Group} from "@core/api/types";

export const useUserStore = defineStore("user", () => {
  const currentUser = ref<Awaited<ReturnType<typeof profileInfo>> | null>(null);
  const isLoaded = ref(false);

  const availableRoles = computed<Group[]>(() => currentUser.value?.groups ?? ["Reader"]);

  const isAdmin = computed(() => currentUser.value?.current_role === "Admin");
  const isLibrarian = computed(() => currentUser.value?.current_role === "Librarian");
  const isReader = computed(() => currentUser.value?.current_role === "Reader");

  async function fetchProfile() {
    const auth = useAuthStore();
    if (!(await auth.updateTokens())) return;
    try {
      currentUser.value = await profileInfo();
      isLoaded.value = true;
    } catch {
      currentUser.value = null;
      isLoaded.value = false;
    }

    if (currentUser.value?.current_role === null || currentUser.value?.current_role === "") {
      currentUser.value.current_role = "None"
    }
  }

  function clearUser() {
    currentUser.value = null;
    isLoaded.value = false;
  }

  async function setCurrentRole(role: Group) {
    if (
      availableRoles.value.includes(role) &&
      availableRoles.value.includes("Admin") &&
      role === "Librarian"
    ) {
      await setRole("Admin");
    } else if (availableRoles.value.includes(role) && role === "Librarian") {
      await setRole("librarian");
    }

    await fetchProfile();
  }

  return {
    currentUser,
    isLoaded,
    availableRoles,
    isAdmin,
    isLibrarian,
    isReader,
    fetchProfile,
    clearUser,
    setCurrentRole,
  };
});
