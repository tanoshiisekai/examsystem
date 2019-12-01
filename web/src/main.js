import Vue from "vue";
import App from "./App";
import router from "./router";
import axios from "axios";
import VueAxios from "vue-axios";
import VueCookie from "vue-cookie";
import { backendhost, backendport } from "./conf";
import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";
import "material-design-icons/iconfont/material-icons.css";
import md5 from "js-md5";


Vue.use(VueMaterial);
Vue.use(VueAxios, axios);
Vue.use(VueCookie);
Vue.prototype.$md5 = md5;

axios.defaults.baseURL = "http://" + backendhost + ":" + backendport;
/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  template: "<App/>",
  components: { App }
});
