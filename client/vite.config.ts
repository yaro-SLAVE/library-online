import { existsSync } from "node:fs";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import { nodePolyfills } from 'vite-plugin-node-polyfills';

const backendPort = process.env.BACKEND_PORT || "8000";
const backendHost = existsSync("/.dockerenv") ? "library-service" : "127.0.0.1";
const proxyTarget = `http://${backendHost}:${backendPort}`;

function normalizeBasePath(path: string | undefined): string {
  if (!path || path === "/") {
    return "/";
  }

  const withLeadingSlash = path.startsWith("/") ? path : `/${path}`;
  return withLeadingSlash.endsWith("/") ? withLeadingSlash : `${withLeadingSlash}/`;
}

const basePath = normalizeBasePath(process.env.VITE_BASE_PATH);

export default defineConfig({
  base: basePath,
  plugins: [
    vue(),
    nodePolyfills(),
  ],
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
        changeOrigin: false,
      },
      "/admin": {
        target: proxyTarget,
        changeOrigin: false,
      },
      "/static": {
        target: proxyTarget,
        changeOrigin: false,
      },
      "/media": {
        target: proxyTarget,
        changeOrigin: false,
      },
    },
  },
});
