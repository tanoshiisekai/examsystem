<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">修改密码</span>
    </md-subheader>
    <md-field>
      <label>请输入原密码</label>
      <md-input v-model="oldpassword" type="password"></md-input>
    </md-field>
    <md-field>
      <label>请输入新密码</label>
      <md-input v-model="password" type="password"></md-input>
    </md-field>
    <md-field>
      <label>请输入确认密码</label>
      <md-input v-model="repassword" type="password"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="changepassword()">确定</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "adminsettings",
  components: {
    AdminMenu
  },
  data() {
    return {
      oldpassword: "",
      password: "",
      repassword: "",
      message: "",
      showSnackbar: false
    };
  },
  methods: {
    changepassword() {
      if (this.password != this.repassword) {
        this.showSnackbar = true;
        this.message = "两次密码输入不一致，请重新输入！";
        return;
      }
      console.log(this.oldpassword.length);
      if (
        this.oldpassword.length == 0 ||
        this.password.length == 0 ||
        this.repassword.length == 0
      ) {
        this.showSnackbar = true;
        this.message = "输入内容不能为空！";
        return;
      }
      var oldpassword = this.$md5(this.oldpassword);
      var newpassword = this.$md5(this.password);
      var token = this.$cookie.get("usertoken");
      this.axios
        .get("/AdminSettings"+apiversion+"/" + token + "/" + oldpassword + "/" + newpassword)
        .then(response => {
          this.showSnackbar = true;
          this.message = response.data["infomsg"];
          this.oldpassword = "";
          this.password = "";
          this.repassword = "";
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.mybutton {
  border: 1px solid #cccccc;
}
</style>
