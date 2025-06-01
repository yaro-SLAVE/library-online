import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import { computed, ref } from "vue";
import type { ProfileInfo, Group } from "@api/types";
import { profileInfo } from "@api/profile";

export const useAuthStore = defineStore("auth", () => {
  type Token = string | undefined;

  const access = useLocalStorage<Token>("accessToken", undefined);
  const refresh = useLocalStorage<Token>("refreshToken", undefined);

  const isAuthenticated = computed(() => refresh.value !== undefined);

  const currentUser = ref<ProfileInfo>();

  const currentUserRole = computed((): Group => {
    if (!currentUser.value) return "Reader";
    if (currentUser.value.groups.includes("Librarian")) {
      return "Reader";
    }
    return "Reader";
  });

  type Tokens = {
    access: string;
    refresh: string;
  };

  function isTokenValid(token: Token): boolean {
    if (token === undefined) {
      return false;
    } else {
      const decoded = jwtDecode(token);
      return Date.now() < decoded.exp! * 1000;
    }
  }

  async function refreshTokens(): Promise<boolean> {
    try {
      const simpleAxios = axios.create();
      const { data } = await simpleAxios.post<Tokens>("/api/auth/refresh/", {
        refresh: refresh.value,
      });

      access.value = data.access;
      refresh.value = data.refresh;
      return true;
    } catch {
      return false;
    }
  }

  async function updateTokens(): Promise<boolean> {
    if (!isTokenValid(refresh.value)) {
      refresh.value = undefined;
      access.value = undefined;
      currentUser.value = undefined;
      return false;
    } else if (!isTokenValid(access.value)) {
      return await refreshTokens();
    }
    return true;
  }

  async function updateProfileInfo() {
    if (await updateTokens()) {
      try {
        currentUser.value = await profileInfo();
      } catch {
        // TODO: check if the error is actually related to the tokens
        refresh.value = undefined;
        access.value = undefined;
        currentUser.value = undefined;
      }
    }
  }

  async function login(username: string, password: string): Promise<boolean> {
    try {
      const simpleAxios = axios.create();
      const { data } = await simpleAxios.post<Tokens>("/api/auth/login/", {
        username: username,
        password: password,
      });
      refresh.value = data.refresh;
      access.value = data.access;
      await updateProfileInfo();
      return true;
    } catch {
      return false;
    }
  }

  async function thirdPartyLogin(externalToken: string): Promise<boolean> {
    try {
      const simpleAxios = axios.create();
      const { data } = await simpleAxios.post<Tokens>("/api/auth/third-party/", {
        token: externalToken,
      });
      refresh.value = data.refresh;
      access.value = data.access;
      await updateProfileInfo();
      return true;
    } catch {
      return false;
    }
  }

  async function bitrixLogin(code: string): Promise<boolean> {
    try {
      const simpleAxios = axios.create();
      const { data } = await simpleAxios.post<Tokens>("/api/auth/bitrix-login/", {
        code: code,
      });
      refresh.value = data.refresh;
      access.value = data.access;
      await updateProfileInfo();
      return true;
    } catch {
      return false;
    }
  }

  async function logout() {
    const refreshCopy = refresh.value;
    refresh.value = undefined;
    access.value = undefined;
    currentUser.value = undefined;

    const simpleAxios = axios.create();
    await simpleAxios.post("/api/auth/logout/", {
      refresh: refreshCopy,
    });
  }

  return {
    isAuthenticated,
    currentUser,
    access,
    refresh,
    updateTokens,
    updateProfileInfo,
    login,
    bitrixLogin,
    logout,
    thirdPartyLogin,
    currentUserRole,
  };
});
