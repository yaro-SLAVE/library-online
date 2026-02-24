import { type App } from 'vue';
import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios';
//@ts-ignore
import qs from 'qs';
import { useAuthStore } from "@core/store/auth";

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

function normalizeBasePath(path: string | undefined): string {
  if (!path) {
    return "/";
  }

  let normalized = path.trim();

  if (!normalized.startsWith("/")) {
    normalized = `/${normalized}`;
  }

  if (!normalized.endsWith("/")) {
    normalized = `${normalized}/`;
  }

  return normalized;
}

export const api: AxiosInstance = axios.create({
  baseURL: normalizeBasePath(import.meta.env.VITE_API_PREFIX),
  paramsSerializer: params => {
    return qs.stringify(params, {
      arrayFormat: "comma"
    });
  }
});

api.interceptors.request.use(async (config: InternalAxiosRequestConfig) => {
  const authStore = useAuthStore();

  if (await authStore.updateTokens()) {
    config.headers.Authorization = `Bearer ${authStore.access}`;
  }

  return config;
}, (error) => {
  return Promise.reject(error);
});

export default {
  install(app: App) {
    app.config.globalProperties.$axios = axios;
    app.config.globalProperties.$api = api;
  }
};
