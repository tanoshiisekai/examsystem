<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span
        class="md-title"
      >易错题整理（共 {{this.wrongcount}} 题，第 {{this.wrongposi}} 题，错误人数 {{this.problem.problem_summarycount}}人）</span>
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
          style="font-size:20px;width:100%;"
        >A. {{this.problem.problem_choiceA}}</md-checkbox>
        <md-checkbox
          v-model="disable_B"
          disabled
          style="font-size:20px;width:100%;"
        >B. {{this.problem.problem_choiceB}}</md-checkbox>
        <md-checkbox
          v-model="disable_C"
          disabled
          style="font-size:20px;width:100%;"
        >C. {{this.problem.problem_choiceC}}</md-checkbox>
        <md-checkbox
          v-model="disable_D"
          disabled
          style="font-size:20px;width:100%;"
        >D. {{this.problem.problem_choiceD}}</md-checkbox>
        <md-button class="md-raised md-primary" @click="donext()">下一题</md-button>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "summarydetails",
  components: {
    AdminMenu
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
      var summary_psetname = this.$cookie.get("summary_psetname");
      var summary_pwrongpercent = this.$cookie.get("summary_pwrongpercent");
      this.axios
        .get(
          "/ProblemSet"+apiversion+"/adminsummary/" +
            usertoken +
            "/" +
            summary_psetname +
            "/" +
            summary_pwrongpercent
        )
        .then(response => {
          var resp = response.data;
          this.wronglist = resp["inforesult"];
          this.wrongcount = this.wronglist.length;
          console.log(this.wronglist);
          this.getnextproblem();
        });
    },
    getnextproblem() {
      console.log("posi", this.posi);
      if (this.posi >= this.wronglist.length) {
        this.posi = 0;
      }
      var usertoken = this.$cookie.get("usertoken");
      if (this.wronglist.length == 0) {
        this.$router.push({ name: "adminemptybook" });
      }
      var pid = this.wronglist[this.posi].problem_id;
      this.axios
        .get("/ProblemSet"+apiversion+"/problemsummary/" + usertoken + "/" + pid)
        .then(response => {
          var resp = response.data;
          this.problem = resp["inforesult"];
          console.log(this.problem);
          console.log(this.posi);
          this.problem["problem_summarycount"] = this.wronglist[
            this.posi
          ].problem_count;
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
