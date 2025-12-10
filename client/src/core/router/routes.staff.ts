import DefaultStaffLayout from "@core/layout/DefaultStaffLayout.vue";
export const staffRoutes = [
  {
    path: "/staff",
    component: DefaultStaffLayout,
    children: [
      {
        path: "orders",
        name: "StaffOrdersPage",
        component: () => import("@staff/views/ManageOrdersPage.vue"),
        meta: { roles: ["Librarian", "Admin"], requiresAuth: true },
      },
      {
        path: "profile",
        name: "StaffProfilePage",
        component: () => import("@core/views/ProfilePage.vue"),
        meta: { roles: ["Librarian", "Admin"], requiresAuth: true },
      },
    ],
  },
];
