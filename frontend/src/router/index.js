import { createRouter, createWebHistory } from "vue-router";
import DefaultView from "../views/DefaultView.vue";

const routes = [
  {
    path: "/",
    name: "Default",
    component: DefaultView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
