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

export const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.DEV ? "/" : "/uz/",
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