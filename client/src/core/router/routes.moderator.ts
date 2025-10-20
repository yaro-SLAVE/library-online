import ModeratorLayout from "@core/layout/moderator/ModeratorLayout.vue";
export const moderatorRoutes = [
  {
    path: "/moderator",
    component: ModeratorLayout,
    meta: { role: "Librarian" },
    children: [
      {
        path: "readers",
        name: "readers",
        component: () => import("@modules/moderator/views/ReadersPage.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "orders",
        name: "orders",
        component: () => import("@modules/staff/views/ManageOrdersPage.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "blacklist",
        name: "blacklist",
        component: () => import("@modules/staff/views/ManageOrdersPage.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "settings",
        name: "settings",
        component: () => import("@modules/staff/views/ManageOrdersPage.vue"),
        meta: { requiresAuth: true },
      },
    ],
  },
];
