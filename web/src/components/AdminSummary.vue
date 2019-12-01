<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">易错题统计</span>
    </md-subheader>
    <md-field>
      <label>请输入题库名称</label>
      <md-input v-model="psetname"></md-input>
    </md-field>
    <md-field>
      <label>请输入最低错误累计数（如3，表示有3个人这道题答错了）</label>
      <md-input v-model="pwrongpercent"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="handleSearch()">查询</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "adminsummary",
  components: {
    AdminMenu
  },
  created() {},
  data() {
    return {
      showSnackbar: false,
      message: "",
      psetname: "",
      pwrongpercent: ""
    };
  },
  methods: {
    handleSearch() {
      var usertoken = this.$cookie.get("usertoken");
      this.$cookie.set("summary_psetname", this.psetname);
      this.$cookie.set("summary_pwrongpercent", this.pwrongpercent);
      this.$cookie.set("laststep", "adminsummary");
      this.$router.push({ name: "summarydetails" });
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
