import ModeratorLayout from "@core/layout/ModeratorLayout.vue";
export const moderatorRoutes = [
  {
    path: "/moderator",
    component: ModeratorLayout,
    meta: { role: "Librarian" },
    children: [

    ],
  },
];
