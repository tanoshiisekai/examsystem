<template>
  <div class="container">
    <md-toolbar>
      <md-menu md-direction="bottom-end" :md-offset-x="0" :md-offset-y="0">
        <md-button md-menu-trigger>
          <i class="material-icons">menu</i>
        </md-button>
        <md-menu-content class="menulist">
          <md-menu-item class="menuitem" @click="addproblem">添加题目</md-menu-item>
          <md-menu-item class="menuitem" @click="manageset">题库管理</md-menu-item>
          <md-menu-item class="menuitem" @click="score">积分统计</md-menu-item>
          <md-menu-item class="menuitem" @click="adminsummary">易错题统计</md-menu-item>
          <md-menu-item class="menuitem" @click="adminsettings">修改密码</md-menu-item>
          <md-menu-item class="menuitem" @click="logout">退出</md-menu-item>
        </md-menu-content>
      </md-menu>
      <span class="md-title">欢迎来到龙龙爱考试</span>
    </md-toolbar>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
export default {
  name: "adminmenu",
  data() {
    return {
      showSnackbar: false,
      message: ""
    };
  },
  created: function() {
    this.checkcookie();
  },
  methods: {
    checkcookie() {
      var username = this.$cookie.get("username");
      var usertoken = this.$cookie.get("usertoken");
      this.axios.get("/AdminLogin/checktoken/" + usertoken).then(response => {
        var resp = response.data;
        console.log(resp);
        if (resp["infostatus"] == 0) {
          this.$router.push({ name: "adminlogin" });
        }
      });
    },
    adminsummary(){
      console.log("adminsummary");
      this.checkcookie();
      this.$router.push({name: "adminsummary"});
    },
    addproblem() {
      console.log("addproblem1");
      this.checkcookie();
      this.$router.push({ name: "addproblem1" });
    },
    manageset() {
      console.log("manageset");
      this.checkcookie();
      this.$router.push({ name: "manageset" });
    },
    score() {
      console.log("adminscore");
      this.checkcookie();
      this.$router.push( {name: "adminscore"});
    },
    adminsettings() {
      this.checkcookie();
      console.log("adminsettings");
      this.$router.push({ name: "adminsettings" });
    },
    logout() {
      this.checkcookie();
      var username = this.$cookie.get("username");
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/AdminLogin/logout/" + usertoken + "/" + username)
        .then(response => {
          var resp = response.data;
          this.message = resp["infomsg"];
          this.showSnackbar = true;
          this.$cookie.set("username", "");
          this.$cookie.set("usertoken", "");
          setTimeout(() => {
            this.$router.push({ name: "adminlogin" });
          }, 1000);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.menulist {
  min-height: 376px;
}
.menuitem {
  height: 60px;
}
.menuitem:hover {
  background-color: #eeeeee;
}
</style>
