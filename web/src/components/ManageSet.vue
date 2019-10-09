<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">题库管理</span>
    </md-subheader>
    <md-table md-card>
      <md-table-row>
        <md-table-head style="text-align:center;">题库名称</md-table-head>
        <md-table-head style="text-align:center;">题库描述</md-table-head>
        <md-table-head style="text-align:center;">题目总数</md-table-head>
        <md-table-head style="text-align:center;">操作</md-table-head>
      </md-table-row>

      <md-table-row v-for="dt in datalist" :key="dt.problemset_title">
        <md-table-cell style="text-align:center;">{{dt.problemset_title}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.problemset_desp}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.problemset_count}}</md-table-cell>
        <md-table-cell style="text-align:center;">
          <md-button class="md-raised md-accent" @click="handleDelete(dt.problemset_title)" >删除</md-button>
        </md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
export default {
  name: "manageset",
  components: {
    AdminMenu
  },
  created() {
    this.getdatas();
  },
  data() {
    return {
      datalist: []
    };
  },
  methods: {
    getdatas() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios.get("/ProblemSet/" + usertoken).then(response => {
        var resp = response.data;
        if (resp["infostatus"]) {
            this.datalist = resp["inforesult"];
        }else{
            alert(resp["infomsg"]);
        }
      });
    },
    handleDelete(problemsettitle){
      var usertoken = this.$cookie.get("usertoken");
      this.axios.get("/ProblemSet/remove/" + usertoken + "/" + problemsettitle).then(response => {
        var resp = response.data;
        if (resp["infostatus"] == 1){
          location.reload();
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
