<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">答题中，无法查看错题！</span>
      <md-button class="md-raised md-accent" @click="dostop()">结束当前答题</md-button>
    </md-subheader>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "answering",
  components: {
    UserMenu
  },
  created() {},
  data() {
    return {};
  },
  methods: {
    dostop() {
      var scoreid = this.$cookie.get("answeringid");
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/ProblemSet"+apiversion+"/finishedtime/" + usertoken + "/" + scoreid)
        .then(response => {
            var resp = response.data;
            if(resp["infostatus"] == 1){
                this.$router.push({name: "notebook"});
            }
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
