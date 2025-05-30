import DefaultStaffLayout from "@core/views/DefaultStaffLayout.vue";

export const staffRoutes = [
  {
    path: "/staff",
    component: DefaultStaffLayout,
    meta: { role: "Librarian" },
    children: [
      {
        path: "orders",
        name: "StaffOrdersPage",
        component: () => import("@staff/views/ManageOrdersPage.vue"),
      },
      {
        path: "profile",
        name: "StaffProfilePage",
        component: () => import("@core/views/ProfilePage.vue"),
      },
    ],
  },
];
