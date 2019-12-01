<template>
  <div class="container">
    <md-toolbar>
      <span class="md-title">欢迎来到龙龙爱考试</span>
    </md-toolbar>
    <md-field>
      <label>请输入用户名</label>
      <md-input v-model="username"></md-input>
    </md-field>
    <md-field>
      <label>请输入密码</label>
      <md-input v-model="password" type="password"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="login()">点击登录</md-button>
    <md-button class="md-raised md-primary" @click="gotoregister()">前往注册</md-button>
    <md-button class="md-raised" @click="gotoadminlogin()">管理员登录</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
      showSnackbar: false,
      message: ""
    };
  },
  methods: {
    gotoregister() {
      this.$router.push({ name: "register" });
    },
    gotoadminlogin() {
      this.$router.push({ name: "adminlogin" });
    },
    login() {
      if (this.username.length == 0 || this.password.length == 0) {
        this.showSnackbar = true;
        this.message = "用户名和密码不能为空!";
      }
      var username = this.username;
      var password = this.$md5(this.password);
      this.axios.get("/Login"+apiversion+"/" + username + "/" + password).then(response => {
        var resp = response.data;
        this.showSnackbar = true;
        this.message = resp["infomsg"];
        console.log(resp);
        if (resp["infostatus"] == 1) {
          this.$cookie.set("username", this.username);
          this.$cookie.set("usertoken", resp["inforesult"]["usertoken"]);
          this.$router.push({ name: "problems" });
        }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
