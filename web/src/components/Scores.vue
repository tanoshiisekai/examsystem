<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">积分榜</span>
    </md-subheader>
    <md-table>
      <md-table-row>
        <md-table-head style="text-align:center;">题库名称</md-table-head>
        <md-table-head style="text-align:center;">最新排名</md-table-head>
        <md-table-head style="text-align:center;">测试题目数量</md-table-head>
        <md-table-head style="text-align:center;">答对数量</md-table-head>
        <md-table-head style="text-align:center;">答错数量</md-table-head>
        <md-table-head style="text-align:center;">答题用时(秒)</md-table-head>
        <md-table-head style="text-align:center;">操作</md-table-head>
      </md-table-row>

      <md-table-row v-for="dt in datalist" :key="dt.problemset_id">
        <md-table-cell style="text-align:center;">{{dt.problemset_title}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_rank}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_problemcount}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_right}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_wrong}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_timespan}}</md-table-cell>
        <md-table-cell style="text-align:center;">
          <md-button class="md-raised md-primary" @click="handleShow(dt.problemset_id)">详细排名</md-button>
        </md-table-cell>
      </md-table-row>
    </md-table>
    
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
export default {
  name: "scores",
  components: {
    UserMenu
  },
  created() {
    this.getdata();
  },
  data() {
    return {
      datalist: [],
    };
  },
  methods: {
    getdata() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios.get("/ProblemSet/scores/" + usertoken).then(response => {
        var resp = response.data;
        if (resp["infostatus"] == 1) {
          this.datalist = resp["inforesult"];
        }
      });
    },
    handleShow(problemset_id) {
      this.$cookie.set("rank_problemsetid", problemset_id);
      this.$cookie.set("laststep", "scores");
      this.$router.push({name: "rankdetails"});
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
