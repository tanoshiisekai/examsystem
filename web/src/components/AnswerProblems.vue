<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">答题中</span>
    </md-subheader>
    <md-card-content>
        {{this.problem.problem_desp}}
    </md-card-content>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
export default {
  name: "answerproblems",
  components: {
    UserMenu
  },
  created() {
    this.initproblems();
  },
  data() {
    return {
      problemid: 0,
      showSnackbar: false,
      message: "",
      problem: 0,
    };
  },
  methods: {
    initproblems() {
      var problemsettitle = this.$cookie.get("problemsettitle");
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/ProblemSet/init/" + usertoken + "/" + problemsettitle)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 1) {
            this.problemid = resp["inforesult"];
            this.getfirstproblem();
          } else {
            this.message = resp["infomsg"];
            this.showSnackbar = true;
          }
        });
    },
    getfirstproblem() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/ProblemSet/answer/" + usertoken + "/" + this.problemid)
        .then(response => {
          var resp = response.data;
          console.log(resp);
          if(resp["infostatus"] == 1){
              this.problem = resp["inforesult"];
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
