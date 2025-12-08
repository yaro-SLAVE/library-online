import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { useAuthStore } from "./auth";
import { profileInfo } from "@api/profile";
import type { Group } from "@core/api/types";

export const useUserStore = defineStore("user", () => {
  const currentUser = ref<Awaited<ReturnType<typeof profileInfo>> | null>(null);
  const isLoaded = ref(false);

  const availableRoles = computed<Group[]>(() => currentUser.value?.groups ?? ["Reader"]);

  const currentRole = useLocalStorage<Group>("currentRole", "Reader");

  const isAdmin = computed(() => currentRole.value === "Admin");
  const isLibrarian = computed(() => currentRole.value === "Librarian");
  const isReader = computed(() => currentRole.value === "Reader");

  async function fetchProfile() {
    const auth = useAuthStore();
    if (!(await auth.updateTokens())) return;
    try {
      currentUser.value = await profileInfo();
      isLoaded.value = true;

      if (!availableRoles.value.includes(currentRole.value)) {
        currentRole.value = "Reader";
      }
    } catch {
      currentUser.value = null;
      isLoaded.value = false;
      currentRole.value = "Reader";
    }
  }

  function clearUser() {
    currentUser.value = null;
    isLoaded.value = false;
    currentRole.value = "Reader";
  }

  function setCurrentRole(role: Group) {
    if (
      availableRoles.value.includes(role) &&
      availableRoles.value.includes("Admin") &&
      role === "Librarian"
    ) {
      currentRole.value = "Admin";
    } else if (availableRoles.value.includes(role)) {
      currentRole.value = role;
    }
  }

  return {
    currentUser,
    isLoaded,
    availableRoles,
    currentRole,
    isAdmin,
    isLibrarian,
    isReader,
    fetchProfile,
    clearUser,
    setCurrentRole,
  };
});
