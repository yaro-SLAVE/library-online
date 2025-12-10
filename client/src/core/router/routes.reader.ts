import ReaderLayout from "@core/layout/ReaderLayout.vue";

export const readerRoutes = [
  {
    path: "/",
    component: ReaderLayout,
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("@reader/views/HomePage.vue"),
        meta: { roles: ["Reader"], requiresAuth: false },
      },
      {
        path: "profile",
        name: "ProfilePage",
        component: () => import("@core/views/ProfilePage.vue"),
        meta: { roles: ["Reader"], requiresAuth: false },
      },
      {
        path: "bitrix-auth",
        name: "OauthRedirectPage",
        component: () => import("@reader/views/OauthRedirectPage.vue"),
        meta: { roles: ["Reader"], requiresAuth: false },
      },
      {
        path: "basket",
        name: "BasketPage",
        component: () => import("@reader/views/BasketPage.vue"),
        meta: { roles: ["Reader"], requiresAuth: false },
      },
      {
        path: "order",
        name: "OrderPage",
        component: () => import("@reader/views/OrderPage.vue"),
        meta: { roles: ["Reader"], requiresAuth: true },
      },
      {
        path: "note",
        name: "NotePage",
        component: () => import("@reader/views/NotePage.vue"),
        meta: { roles: ["Reader"], requiresAuth: false },
      },
      {
        path: "orders",
        name: "OrdersPage",
        component: () => import("@reader/views/OrdersPage.vue"),
        meta: { roles: ["Reader"], requiresAuth: true },
      },
    ],
  },
];
