<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">详细积分信息</span>
      <md-button class="md-raised md-accent" style="margin-left:100px;" @click="handleBack()">返回</md-button>
    </md-subheader>
     <md-subheader>
    <span class="md-title" style="margin-top:20px;margin-bottom:20px;">题库名称：{{psettitle}}</span>
     </md-subheader>
    <md-table>
      <md-table-row>
        <md-table-head style="text-align:center;">最新排名</md-table-head>
        <md-table-head style="text-align:center;">用户名</md-table-head>
        <md-table-head style="text-align:center;">测试题目数量</md-table-head>
        <md-table-head style="text-align:center;">答对数量</md-table-head>
        <md-table-head style="text-align:center;">答错数量</md-table-head>
        <md-table-head style="text-align:center;">答题用时(秒)</md-table-head>
      </md-table-row>

      <md-table-row v-for="dt in datalist" :key="dt.user_id">
        <md-table-cell style="text-align:center;">{{dt.score_rank}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.user_name}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_problemcount}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_right}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_wrong}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.score_timespan}}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
export default {
  name: "rankdetails",
  components: {
    UserMenu
  },
  created() {
    this.getdata();
  },
  data() {
    return {
      datalist: [],
      laststep: "",
      psettitle: ""
    };
  },
  methods: {
    getdata() {
      var usertoken = this.$cookie.get("usertoken");
      var psetid = this.$cookie.get("rank_problemsetid");
      this.axios
        .get("/ProblemSet/scoreslist/" + usertoken + "/" + psetid)
        .then(response => {
            var resp = response.data;
            console.log(resp);
            if(resp["infostatus"] == 1){
                this.datalist = resp["inforesult"];
                this.psettitle = this.datalist[0].problemset_title;
            }
        });
    },
    handleBack() {
      this.laststep = this.$cookie.get("laststep");
      this.$router.push({ name:this.laststep });
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
