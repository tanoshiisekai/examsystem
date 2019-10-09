<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">修改密码</span>
    </md-subheader>
    <md-field>
      <label>请输入原密码</label>
      <md-input v-model="oldpassword"  type="password"></md-input>
    </md-field>
    <md-field>
      <label>请输入新密码</label>
      <md-input v-model="password"  type="password"></md-input>
    </md-field>
    <md-field>
      <label>请输入确认密码</label>
      <md-input v-model="repassword"  type="password"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="changepassword()">确定</md-button>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
export default {
  name: "adminsettings",
  components: {
    AdminMenu
  },
  data() {
    return {
        oldpassword: "",
        password: "",
        repassword: ""
    };
  },
  methods: {
    changepassword(){
        alert("未实现");
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
