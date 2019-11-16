<template>
  <div class="container">
    <md-toolbar>
      <md-menu md-direction="bottom-end" :md-offset-x="0" :md-offset-y="0">
        <md-button md-menu-trigger>
          <i class="material-icons">menu</i>
        </md-button>
        <md-menu-content class="menulist">
          <md-menu-item class="menuitem" @click="problems">答题</md-menu-item>
          <md-menu-item class="menuitem" @click="notes">错题本</md-menu-item>
          <md-menu-item class="menuitem" @click="scores">积分榜</md-menu-item>
          <md-menu-item class="menuitem" @click="usersettings">修改密码</md-menu-item>
          <md-menu-item class="menuitem" @click="userlogout">退出</md-menu-item>
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
  name: "usermenu",
  data() {
    return {
      showSnackbar: false,
      message: ""
    };
  },
  created: function() {
    document.οncοntextmenu = function() {
      return false;
    };
    document.onselectstart = function() {
      return false;
    };
    var username = this.$cookie.get("username");
    var usertoken = this.$cookie.get("usertoken");
    if (!username || !usertoken) {
      this.$router.push({ name: "login" });
    }
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
    problems() {
      console.log("problems");
      this.$router.push({ name: "problems" });
    },
    notes() {
      console.log("notebook");
      this.$router.push({ name: "notebook" });
    },
    scores() {
      console.log("scores");
      this.$router.push({ name: "scores" });
    },
    usersettings() {
      console.log("usersettings");
      this.$router.push({ name: "usersettings" });
    },
    userlogout() {
      var username = this.$cookie.get("username");
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/Login/logout/" + usertoken + "/" + username)
        .then(response => {
          var resp = response.data;
          this.message = resp["infomsg"];
          this.showSnackbar = true;
          this.$cookie.set("username", "");
          this.$cookie.set("usertoken", "");
          setTimeout(() => {
            this.$router.push({ name: "login" });
          }, 1000);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.menulist {
  min-height: 316px;
}
.menuitem {
  height: 60px;
}
.menuitem:hover {
  background-color: #eeeeee;
}
</style>
