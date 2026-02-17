import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { useAuthStore } from "./auth";
import { profileInfo, setRole } from "@api/profile";
import { userRoles, type Group, type UserRoleEnum } from "@core/api/types";

export const useUserStore = defineStore("user", () => {
  const currentUser = ref<Awaited<ReturnType<typeof profileInfo>> | null>(null);
  const isLoaded = ref(false);

  const availableRoles = computed<Group[]>(() => currentUser.value?.groups ?? ["Reader"]);

  const currentRole = computed(() => currentUser.value?.current_role ? currentUser.value?.current_role : userRoles.reader);

  const isAdmin = computed(() => currentUser.value?.current_role === "Admin");
  const isLibrarian = computed(() => currentUser.value?.current_role === "Librarian");
  const isReader = computed(() => currentUser.value?.current_role === "Reader");

  async function fetchProfile() {
    const auth = useAuthStore();
    if (!(await auth.updateTokens())) return;
    try {
      currentUser.value = await profileInfo();
      isLoaded.value = true;

      // if (!availableRoles.value.includes(currentRole.value)) {
      //   currentRole.value = "Reader";
      // }
    } catch {
      currentUser.value = null;
      isLoaded.value = false;
      // currentRole.value = "Reader";
    }
  }

  function clearUser() {
    currentUser.value = null;
    isLoaded.value = false;
    // currentRole.value = "Reader";
  }

  async function setCurrentRole(role: Group) {
    if (
      availableRoles.value.includes(role) &&
      availableRoles.value.includes("Admin") &&
      role === "Librarian"
    ) {
      await setRole(userRoles.admin);
    } else if (availableRoles.value.includes(role) && role === "Librarian") {
      await setRole(userRoles.librarian);
    }

    await fetchProfile();
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
