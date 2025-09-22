import { createRouter, createWebHistory } from "vue-router";
import { readerRoutes } from "@core/router/routes.reader";
import { staffRoutes } from "@core/router/routes.staff";
import { useAuthStore } from "@core/store/auth";
import { storeToRefs } from "pinia";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...readerRoutes,
    ...staffRoutes,
    {
      path: "/:pathMatch(.*)*",
      redirect: "/",
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const { currentUserRole } = storeToRefs(authStore);
  const requiredRole = to.meta.role;
  if (authStore.isCurrentUserInit === undefined) {
    await authStore.updateProfileInfo();
  }
  // if(requiredAuth && !authStore.isAuthenticated) {
  //   return next ("/");
  // }

  if (!authStore.currentUser) {
    await authStore.updateProfileInfo();
  }

  if (!requiredRole) {
    return next();
  }

  if (currentUserRole.value === requiredRole) {
    return next();
  }

  if (currentUserRole.value === "Reader") {
    return next("/");
  } else if (currentUserRole.value === "Librarian") {
    return next("/staff/orders");
  } else {
    return next("/");
  }
});

export default router;
