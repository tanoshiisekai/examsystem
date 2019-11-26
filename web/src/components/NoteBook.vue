<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">错题本（ 共 {{this.wrongcount}} 题，第 {{this.wrongposi}} 题 ）</span>
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
          v-model="disable_A"
          disabled
          style="font-size:20px;width:100%;height:50px;"
        >A. {{this.problem.problem_choiceA}}</md-checkbox>
        <md-checkbox
          v-model="disable_B"
          disabled
          style="font-size:20px;width:100%;height:50px;"
        >B. {{this.problem.problem_choiceB}}</md-checkbox>
        <md-checkbox
          v-model="disable_C"
          disabled
          style="font-size:20px;width:100%;height:50px;"
        >C. {{this.problem.problem_choiceC}}</md-checkbox>
        <md-checkbox
          v-model="disable_D"
          disabled
          style="font-size:20px;width:100%;height:50px;"
        >D. {{this.problem.problem_choiceD}}</md-checkbox>
        <md-button class="md-raised md-accent" @click="doremove()">移除该题</md-button>
        <md-button class="md-raised md-primary" @click="donext()">下一题</md-button>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
import { filehost, fileport } from "@/conf";
export default {
  name: "notebook",
  components: {
    UserMenu
  },
  created() {
    this.getwrongidlist();
  },
  data() {
    return {
      wronglist: [],
      posi: 0,
      problem: { "": "" },
      disable_A: false,
      disable_B: false,
      disable_C: false,
      disable_D: false,
      wrongcount: 0,
      wrongposi: 1
    };
  },
  methods: {
    doremove() {
      console.log(this.posi);
      this.posi = this.posi - 1;
      var nbid = this.wronglist[this.posi].notebookid;
      console.log(nbid);
      var usertoken = this.$cookie.get("usertoken");
      console.log(this.wronglist);
      this.axios
        .get("/ProblemSet/wrongproblem/" + usertoken + "/" + nbid)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 1) {
            this.wronglist.splice(this.posi, 1);
            console.log(this.wronglist);
            this.wrongcount = this.wronglist.length;

            console.log(this.posi);
            console.log(this.wrongposi);
            this.donext();
          }
        });
    },
    donext() {
      this.disable_A = false;
      this.disable_B = false;
      this.disable_C = false;
      this.disable_D = false;
      this.getnextproblem();
    },
    getwrongidlist() {
      this.wrongidlist = [];
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/ProblemSet/problemanswer/" + usertoken)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == -1) {
            this.$cookie.set("answeringid", resp["inforesult"]);
            this.$router.push({ name: "answering" });
          }
          this.wronglist = resp["inforesult"];
          this.wrongcount = this.wronglist.length;
          console.log(this.wronglist);
          this.getnextproblem();
        });
    },
    getnextproblem() {
      if (this.posi >= this.wronglist.length) {
        this.posi = 0;
      }
      var usertoken = this.$cookie.get("usertoken");
      if (this.wronglist.length == 0) {
        this.$router.push({ name: "emptybook" });
      }
      var pid = this.wronglist[this.posi].problemid;
      this.axios
        .get("/ProblemSet/problemanswer/" + usertoken + "/" + pid)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 3){
            alert(resp["infomsg"]);
            this.$router.push({name:"emptybook"});
          }
          console.log(resp["infomsg"]);
          if (resp["infostatus"] == -1) {
            setTimeout(() => {
              this.$router.push({ name: "noteterminated" });
            }, 1000);
          }
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
          var panswer = this.problem.problem_answer;
          for (var i in panswer) {
            if (panswer[i] == "A") {
              this.disable_A = true;
            }
            if (panswer[i] == "B") {
              this.disable_B = true;
            }
            if (panswer[i] == "C") {
              this.disable_C = true;
            }
            if (panswer[i] == "D") {
              this.disable_D = true;
            }
          }
          this.wrongposi = this.posi + 1;
          this.posi = this.posi + 1;
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
