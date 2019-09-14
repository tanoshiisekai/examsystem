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
    <md-button class="md-raised md-accent" @click="onlogin()">点击登录</md-button>
    <md-button class="md-raised" @click="gotouserlogin()">返回用户登录</md-button>
  </div>
</template>

<script>
export default {
  name: "adminlogin",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    onlogin() {
      if (this.username.length == 0) {
        alert("请输入用户名！");
        return;
      }
      if (this.password.length == 0) {
        alert("请输入密码！");
        return;
      }
      this.axios
        .get("/AdminLogin/" + this.username + "/" + this.password)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 1) {
            this.$cookie.set("username", this.username);
            this.$cookie.set("usertoken", resp["inforesult"]["usertoken"]);
            this.$router.push({ name: "addproblem1" });
          } else {
            alert(resp["infomsg"]);
          }
        });
    },
    gotouserlogin() {
      this.$router.push({ name: "adminlogin" });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
