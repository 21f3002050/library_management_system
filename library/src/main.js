import { createApp } from "vue";
import App from "./App.vue";
import router from "./routes";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:5000";
const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

const app = createApp(App);

app.config.globalProperties.$axios = axiosInstance;
app.use(router);
app.mount("#app");
