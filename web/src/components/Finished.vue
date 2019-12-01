<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-card>
      <md-card-header>
        <md-card-header-text style="text-align:left;">
          <div class="md-title" style="font-size:30px;">答题结束</div>
        </md-card-header-text>
      </md-card-header>
    </md-card>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
 import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "answerproblems",
  components: {
    UserMenu
  },
  created() {
    document.onmousemove = null;
    this.settimestr();
  },
  data() {
    return {};
  },
  methods: {
    settimestr() {
      var usertoken = this.$cookie.get("usertoken");
      var scoreid = this.$cookie.get("scoreid");
      this.axios
        .get("/ProblemSet"+apiversion+"/finishedtime/" + usertoken + "/" + scoreid)
        .then(response =>{
          var resp = response.data;
          console.log(resp);
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
