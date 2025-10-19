import { createRouter, createWebHistory } from "vue-router";
import { readerRoutes } from "@core/router/routes.reader";
import { staffRoutes } from "@core/router/routes.staff";
import { moderatorRoutes } from "./routes.moderator";
import { useAuthStore } from "@core/store/auth";
import { useUserStore } from "@core/store/user";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...readerRoutes, ...staffRoutes, ...moderatorRoutes],
});

const roleHomeRoutes: Record<string, string> = {
  Reader: "/",
  Librarian: "/staff/orders",
  Admin: "/moderator/readers",
};

let lastProfileCheck = 0;
const PROFILE_CHECK_INTERVAL = 1 * 60 * 1000; // 1 минута

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  const user = useUserStore();

  if (!auth.isAuthenticated) {
    if (!to.meta.requiresAuth) return next();
    return next("/profile");
  }

  const tokensOk = await auth.updateTokens();
  if (!tokensOk) {
    await auth.logout();
    return next("/profile");
  }

  const now = Date.now();
  if (!user.isLoaded || now - lastProfileCheck > PROFILE_CHECK_INTERVAL) {
    await user.fetchProfile();
    lastProfileCheck = now;
  }

  const requiredRoles = to.matched
    .map(r => r.meta.roles)
    .find(r => r !== undefined) as string[] | undefined;

  if (requiredRoles?.includes(user.currentRole)) {
    return next();
  }

  const fallback = roleHomeRoutes[user.currentRole] ?? "/";
  return next(fallback);
});

export default router;
