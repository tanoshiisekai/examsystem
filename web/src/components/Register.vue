<template>
  <div class="container">
    <md-toolbar>
      <span class="md-title">注册新用户</span>
    </md-toolbar>
    <md-field>
      <label>请输入用户名</label>
      <md-input v-model="username"></md-input>
    </md-field>
    <md-field>
      <label>请输入密码</label>
      <md-input v-model="password" type="password"></md-input>
    </md-field>
    <md-field>
      <label>请输入确认密码</label>
      <md-input v-model="repassword" type="password"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="register()">点击注册</md-button>
    <md-button class="md-raised" @click="gotologin()">返回登录</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "register",
  data() {
    return {
      username: "",
      password: "",
      repassword: "",
      showSnackbar: false,
      message: ""
    };
  },
  methods: {
    gotologin() {
      this.$router.push({ name: "login" });
    },
    register() {
      if (this.password != this.repassword) {
        this.showSnackbar = true;
        this.message = "两次密码输入不一致，请重新输入！";
        return;
      }
      if (
        this.username.length == 0 ||
        this.password.length == 0 ||
        this.repassword.length == 0
      ) {
        this.showSnackbar = true;
        this.message = "输入内容不能为空!";
        return;
      }
      var username = this.username;
      var password = this.$md5(this.password);
      this.axios
        .get("/Register"+apiversion+"/" + username + "/" + password)
        .then(response => {
          this.showSnackbar = true;
          this.message = response.data["infomsg"];
          this.username = "";
          this.password = "";
          this.repassword = "";
          if(response.data["infostatus"] == 1){
            setTimeout(() => {
            this.$router.push({ name: "login" });
          }, 2000);
          }
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
