import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import { computed } from "vue";

export const useAuthStore = defineStore("auth", () => {
  type Token = string | undefined;
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

  const access = useLocalStorage<Token>("accessToken", undefined);
  const refresh = useLocalStorage<Token>("refreshToken", undefined);
  const isAuthenticated = computed(() => refresh.value !== undefined);

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
      return false;
    } else if (!isTokenValid(access.value)) {
      return await refreshTokens();
    }
    return true;
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
      return true;
    } catch {
      return false;
    }
  }

  async function logout() {
    const refreshCopy = refresh.value;
    refresh.value = undefined;
    access.value = undefined;

    const simpleAxios = axios.create();
    await simpleAxios.post("/api/auth/logout/", {
      refresh: refreshCopy,
    });
  }

  return {
    isAuthenticated,
    access,
    refresh,
    updateTokens,
    login,
    bitrixLogin,
    logout,
  };
});
