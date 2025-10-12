import DefaultStaffLayout from "@core/layout/DefaultStaffLayout.vue";
import AdminView from "@modules/staff/views/AdminView.vue";
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
        meta: { requiresAuth: true },
      },
      {
        path: "profile",
        name: "StaffProfilePage",
        component: () => import("@core/views/ProfilePage.vue"),
        meta: { requiresAuth: true },
      },
    ],
  },
];
