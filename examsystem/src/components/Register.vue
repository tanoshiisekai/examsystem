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
      <md-input v-model="password"></md-input>
    </md-field>
    <md-field>
      <label>请输入确认密码</label>
      <md-input v-model="repassword"></md-input>
    </md-field>
    <md-button class="md-raised md-accent">点击注册</md-button>
    <md-button class="md-raised" @click="gotologin()">返回登录</md-button>
  </div>
</template>

<script>
export default {
  name: "register",
  data() {
    return {
      username: "",
      password: "",
      repassword: ""
    };
  },
  methods: {
    gotologin() {
      this.$router.push({ name: "login" });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
