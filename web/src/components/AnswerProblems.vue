<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">答题中</span>
    </md-subheader>
    <md-card>
      <md-card-header>
        <md-card-header-text style="text-align:left;">
          <div class="md-title" style="font-size:30px;">{{this.problem.problem_desp}}</div>
        </md-card-header-text>
      </md-card-header>
      <md-card-content style="text-align:left;">
        <md-card-media style="text-align:left;">
          <img :src="this.problem.problem_picpath" style="width:300px;" />
        </md-card-media>
        <md-checkbox
          v-model="array"
          value="A"
          style="font-size:20px;width:100%;"
        >A. {{this.problem.problem_choiceA}}</md-checkbox>
        <md-checkbox
          v-model="array"
          value="B"
          style="font-size:20px;width:100%;"
        >B. {{this.problem.problem_choiceB}}</md-checkbox>
        <md-checkbox
          v-model="array"
          value="C"
          style="font-size:20px;width:100%;"
        >C. {{this.problem.problem_choiceC}}</md-checkbox>
        <md-checkbox
          v-model="array"
          value="D"
          style="font-size:20px;width:100%;"
        >D. {{this.problem.problem_choiceD}}</md-checkbox>
        <md-button class="md-raised md-primary" @click="submitanswer()">提交</md-button>
      </md-card-content>
    </md-card>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
import { filehost, fileport } from "@/conf";
export default {
  name: "answerproblems",
  components: {
    UserMenu
  },
  created() {
    window.onbeforeunload = function(e) {
      e = e || window.event;
      // 兼容IE8和Firefox 4之前的版本
      if (e) {
        e.returnValue = "刷新提示";
      }
      // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
      return "刷新提示";
    };
    this.initproblems();
  },
  mounted() {
    if (window.performance.navigation.type == 1) {
      // 截断刷新
      console.log("刷新");
    }
  },
  data() {
    return {
      problemid: 0,
      showSnackbar: false,
      message: "",
      problem: 0,
      array: []
    };
  },
  methods: {
    submitanswer() {
      var answer = this.array;
      answer.sort();
      answer = answer.join("");
      var result = this.$md5(
        this.$md5(answer + this.problem.problem_id) + answer
      );
      if (result == this.problem.problem_answer) {
        console.log("right");
      } else {
        console.log("wrong");
      }
    },
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
          if (resp["infostatus"] == 1) {
            this.problem = resp["inforesult"];
            if (this.problem.problem_picpath.length > 0) {
              this.problem.problem_picpath =
                "http://" +
                filehost +
                ":" +
                fileport +
                "/" +
                this.problem.problem_picpath;
            } else {
              this.problem.problem_picpath = "";
            }
            console.log(this.problem);
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
