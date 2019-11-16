<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">积分统计</span>
    </md-subheader>
    <md-field>
      <label>请输入题库名称</label>
      <md-input v-model="psetname"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="handleSearch()">查询</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
export default {
  name: "adminscore",
  components: {
    AdminMenu
  },
  created() {},
  data() {
    return {
      showSnackbar: false,
      message: "",
      psetname: ""
    };
  },
  methods: {
    handleSearch() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/ProblemSet/pset/" + usertoken + "/" + this.psetname)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 1) {
            this.$cookie.set("rank_problemsetid", resp["inforesult"]);
            this.$cookie.set("laststep", "adminscore");
            this.$router.push({name: "rankdetails"});
          } else {
            this.showSnackbar = true;
            this.message = resp["infomsg"];
          }
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
