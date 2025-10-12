import ModeratorLayout from "@core/layout/moderator/ModeratorLayout.vue";
export const moderatorRoutes = [
  {
    path: "/moderator",
    component: ModeratorLayout,
    meta: { role: "Librarian" },
    children: [
      {
        path: "some",
        name: "some",
        component: () => import("@modules/moderator/views/Someview.vue"),
        meta: { requiresAuth: true },
      },
    ],
  },
];
