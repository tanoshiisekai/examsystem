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
      <md-input v-model="password"></md-input>
    </md-field>
    <md-button class="md-raised md-accent">点击登录</md-button>
    <md-button class="md-raised" @click="gotoregister()">前往注册</md-button>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    gotoregister() {
      this.$router.push({ name: "register" });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
