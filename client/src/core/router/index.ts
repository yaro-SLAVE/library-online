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

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  const user = useUserStore();

  
  return next()
});

export default router;
