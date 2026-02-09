import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const proxyTarget = env.VITE_PROXY_TARGET || "http://127.0.0.1:8000";

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@assets': fileURLToPath(new URL('./src/assets', import.meta.url)),

        '@core': fileURLToPath(new URL('./src/core', import.meta.url)),
        '@api': fileURLToPath(new URL('./src/core/api', import.meta.url)),
        '@components': fileURLToPath(new URL('./src/core/components', import.meta.url)),
        '@layouts': fileURLToPath(new URL('./src/core/layouts', import.meta.url)),
        '@store': fileURLToPath(new URL('./src/core/store', import.meta.url)),

        '@modules': fileURLToPath(new URL('./src/modules', import.meta.url)),
        '@reader': fileURLToPath(new URL('./src/modules/reader', import.meta.url)),
        '@staff': fileURLToPath(new URL('./src/modules/staff', import.meta.url)),
        '@moderator': fileURLToPath(new URL('./src/modules/moderator', import.meta.url)),
        '@utils': fileURLToPath(new URL('./src/core/utils', import.meta.url)),
      }
    },

    css: {
      preprocessorOptions: {
        scss: {
          api: "modern-compiler",
        },
      },
    },

    server: {
      proxy: {
        "/api": {
          target: proxyTarget,
        },
        "/admin": {
          target: proxyTarget,
        },
        "/static": {
          target: proxyTarget,
        },
        "/media": {
          target: proxyTarget,
        },
      },
    },
  };
});
