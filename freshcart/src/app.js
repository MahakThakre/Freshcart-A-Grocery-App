import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import store from "./store/store.js";
import App from "./App.vue";
import "bootstrap-icons/font/bootstrap-icons.css";
import welcome from "./components/welcome.vue";
import manager_signup from "./components/manager_signup.vue";
import manager_dashboard from "./components/manager_dashboard.vue";
import user_signup from "./components/usersignup.vue";
import admin_login from "./components/admin_login.vue";
import user_login from "./components/user_login.vue";
import manager_login from "./components/manager_login.vue";
import admin_dashboard from "./components/admin_dashboard.vue";
import category_products from "./components/category_products.vue";
import single_product from "./components/single_product.vue";
import user_dashboard from "./components/user_dashboard.vue";
import buy_product from "./components/buy_product.vue";
import add_to_cart from "./components/cart.vue";
import CartBuy from "./components/cart_buy.vue";
import boughtProducts from "./components/view_buy_prod.vue";
import searchProduct from "./components/search.vue";
import UserProfile from "./components/userProfile.vue";
import ViewProducts from "./components/Products.vue";

const routes = [
  { path: "/", component: welcome },
  { path: "/manager_signup", component: manager_signup },
  {
    path: "/searchProducts",
    component: searchProduct,
    name: searchProduct,
    props: true,
  },
  {
    path: "/manager_dashboard/:email",
    component: manager_dashboard,
    props: true,
  },
  {
    path: "/boughtProducts",
    component: boughtProducts,
    name: boughtProducts,
    props: true,
  },
  {
    path: "/buy_product/:category_id/:product_id",
    component: buy_product,
    name: "buy_product",
    props: true,
  },
  {
    path: "/cart-buy",
    name: "cart-buy",
    component: CartBuy,
  },
  {
    path: "/add_to_cart/:category_id/:product_id",
    component: add_to_cart,
    name: "cart",
    props: true,
  },
  {
    path: "/user_dashboard/:email",
    component: user_dashboard,
    props: true,
  },
  { path: "/user_signup", component: user_signup },
  { path: "/admin_login", component: admin_login },
  { path: "/user_login", component: user_login },
  { path: "/manager_login", component: manager_login },
  { path: "/admin_dashboard/:email", component: admin_dashboard, props: true },
  {
    path: "/category_products/:category_id",
    component: category_products,
    name: "category_products",
    props: true,
  },
  {
    path: "/profile",
    name: "UserProfile",
    component: UserProfile,
    props: true,
  },
  {
    path: "/single_product/:category_id/:product_id",
    component: single_product,
    name: "single_product",
    props: true,
  },
  {
    path: "/getProductsPage/:category_id",
    component: ViewProducts,
    name: "viewProducts",
    props: true,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.use(router);
app.use(store);

app.mount("#app");
