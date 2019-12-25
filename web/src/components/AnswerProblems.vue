<template>
  <div class="container">
    <div class="virtualbody">
      <md-subheader>
        <span class="md-title">[ {{this.username}} ] 答题中</span>
      </md-subheader>
      <md-subheader>
        <span>注意至少有一个正确答案，选择不全不得分</span>
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
            style="font-size:20px;width:100%;height:50px;"
          >A. {{this.problem.problem_choiceA}}</md-checkbox>
          <md-checkbox
            v-model="array"
            value="B"
            style="font-size:20px;width:100%;height:50px;"
          >B. {{this.problem.problem_choiceB}}</md-checkbox>
          <md-checkbox
            v-model="array"
            value="C"
            style="font-size:20px;width:100%;height:50px;"
          >C. {{this.problem.problem_choiceC}}</md-checkbox>
          <md-checkbox
            v-model="array"
            value="D"
            style="font-size:20px;width:100%;height:50px;"
          >D. {{this.problem.problem_choiceD}}</md-checkbox>
          <md-button
            class="md-raised md-primary"
            @click="doanswer()"
            :disabled="isunable"
            :class="[styles]"
          >提交</md-button>
        </md-card-content>
      </md-card>
      <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
        <span>{{message}}</span>
      </md-snackbar>
    </div>
    <div class="fixedbar">{{this.timecountvalue}}</div>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
import {
  filehost,
  fileport,
  apiversion,
  unmovetime,
  cheattime,
  unmovecount,
  moveoutcount
} from "@/conf";
export default {
  name: "answerproblems",
  components: {
    UserMenu
  },
  created() {
    document.οncοntextmenu = function() {
      return false;
    };
    document.onselectstart = function() {
      return false;
    };
    document.onmousemove = this.mouseMove;
    document.onblur = this.mouseMove;
    document.onvisibilitychange = this.visibilitychange;
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
    this.username = this.$cookie.get("username");
  },
  data() {
    return {
      problemid: 0,
      showSnackbar: false,
      message: "",
      problem: 0,
      array: [],
      timecountvalue: 0,
      timer: null,
      timer1: null,
      scoreid: 0,
      isunable: false,
      lasttimestap: 0,
      warningcount: 0,
      span: 0,
      mousePos: 0,
      outcount: 0,
      username: ""
    };
  },
  methods: {
    visibilitychange() {
      console.log("visibility change");
    },
    getViewPort() {
      if (document.compatMode == "BackCompat") {
        //混杂模式
        return {
          width: document.body.clientWidth,
          height: document.body.clientHeight
        };
      } else {
        return {
          width: document.documentElement.clientWidth,
          height: document.documentElement.clientHeight
        };
      }
    },
    getDocumentPort() {
      if (document.compatMode == "BackCompat") {
        return {
          width: document.body.scrollWidth,
          height: document.body.scrollHeight
        };
      } else {
        return {
          width: Math.max(
            document.documentElement.scrollWidth,
            document.documentElement.clientWidth
          ),
          height: Math.max(
            document.documentElement.scrollHeight,
            document.documentElement.clientHeight
          )
        };
      }
    },
    mouseMove(ev) {
      ev = ev || window.event;
/*       this.mousePos = this.mousePosition(ev);
      if (this.mousePos.x < 10) {
        alert("注意：鼠标请不要离开答题区域！");
        this.outcount = this.outcount + 1;
      }
      if (this.mousePos.x > this.getViewPort()["width"] - 10) {
        alert("注意：鼠标请不要离开答题区域！");
        this.outcount = this.outcount + 1;
      }
      if (this.mousePos.y < 10) {
        alert("注意：鼠标请不要离开答题区域！");
        this.outcount = this.outcount + 1;
      }
      if (this.mousePos.y > this.getViewPort()["height"] - 10) {
        alert("注意：鼠标请不要离开答题区域！");
        this.outcount = this.outcount + 1;
      }
      if (this.outcount > moveoutcount) {
        alert("系统检测到你有作弊嫌疑，请重新答题！");
        this.$router.push({ name: "finished" });
      } */
      var mousetimestamp = new Date().getTime();
      if (this.lasttimestap == 0) {
        this.lasttimestap = mousetimestamp;
      } else {
        this.span = mousetimestamp - this.lasttimestap;
        if (this.span > unmovetime) {
          alert("注意：你已经长时间没有移动鼠标！");
          this.warningcount = this.warningcount + 1;
          if (this.warningcount > unmovecount && this.span > cheattime) {
            alert("系统检测到你有作弊嫌疑，请重新答题！");
            this.$router.push({ name: "finished" });
          } else {
            this.lasttimestap = mousetimestamp;
          }
        } else {
          this.lasttimestap = mousetimestamp;
        }
      }
    },
    mousePosition(ev) {
      if (ev.pageX || ev.pageY) {
        return { x: ev.pageX, y: ev.pageY };
      }
      return {
        x: ev.clientX + document.body.scrollLeft - document.body.clientLeft,
        y: ev.clientY + document.body.scrollTop - document.body.clientTop
      };
    },
    addwrongproblem() {
      var pid = this.problem.problem_id;
      var psid = this.problem.problemset_id;
      console.log("pid", pid);
      console.log("psid", psid);
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get(
          "/ProblemSet" +
            apiversion +
            "/wrongproblem/" +
            usertoken +
            "/" +
            psid +
            "/" +
            pid
        )
        .then(response => {
          var resp = response.data;
          console.log(resp);
        });
    },
    submitanswer() {
      var dotimestamp = new Date().getTime();
      console.log(dotimestamp);
      this.isunable = true;
      this.styles = "changeposition";
      var answer = this.array;
      answer.sort();
      answer = answer.join("");
      console.log(this.answer);
      var result = this.$md5(
        this.$md5(answer + this.problem.problem_id) + answer
      );
      console.log(this.scoreid);
      var usertoken = this.$cookie.get("usertoken");
      if (result == this.problem.problem_answer) {
        var answermd5 = this.$md5(this.$md5(usertoken + "10") + this.scoreid);
        console.log(answermd5);
        this.axios
          .get(
            "/ProblemSet" +
              apiversion +
              "/addscore/" +
              usertoken +
              "/" +
              this.scoreid +
              "/1/0/" +
              answermd5 +
              "/" +
              dotimestamp
          )
          .then(response => {
            var resp = response.data;
            console.log(resp);
            if (resp["infostatus"] == -1) {
              alert("请不要频繁点击按钮！");
              this.isunable = false;
              this.styles = "recoverposition";
            } else {
              clearInterval(this.timer);
              this.timer = null;
              if (this.problem.problem_nextpid != -1) {
                this.problemid = this.problem.problem_nextpid;
                setTimeout(() => {
                  this.getfirstproblem();
                }, 1000);
              } else {
                this.$router.push({ name: "finished" });
              }
            }
          });
      } else {
        var answermd5 = this.$md5(this.$md5(usertoken + "01") + this.scoreid);
        this.axios
          .get(
            "/ProblemSet" +
              apiversion +
              "/addscore/" +
              usertoken +
              "/" +
              this.scoreid +
              "/0/1/" +
              answermd5 +
              "/" +
              dotimestamp
          )
          .then(response => {
            var resp = response.data;
            console.log(resp);
            if (resp["infostatus"] == -1) {
              alert("请不要频繁点击按钮！");
              this.isunable = false;
              this.styles = "recoverposition";
            } else {
              this.addwrongproblem();
              clearInterval(this.timer);
              this.timer = null;
              if (this.problem.problem_nextpid != -1) {
                this.problemid = this.problem.problem_nextpid;
                setTimeout(() => {
                  this.getfirstproblem();
                }, 1000);
              } else {
                this.$router.push({ name: "finished" });
              }
            }
          });
      }
    },
    doanswer() {
      this.submitanswer();
    },
    initproblems() {
      var problemsettitle = this.$cookie.get("problemsettitle");
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get(
          "/ProblemSet" +
            apiversion +
            "/init/" +
            usertoken +
            "/" +
            problemsettitle
        )
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 1) {
            this.problemid = resp["inforesult"][0];
            this.scoreid = resp["inforesult"][1];
            this.$cookie.set("scoreid", this.scoreid);
            this.getfirstproblem();
          } else {
            this.message = resp["infomsg"];
            this.showSnackbar = true;
          }
        });
    },
    getfirstproblem() {
      this.isunable = false;
      this.styles = "recoverposition";
      this.array = [];
      console.log(this.problemid);
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get(
          "/ProblemSet" +
            apiversion +
            "/answer/" +
            usertoken +
            "/" +
            this.problemid
        )
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == -1) {
            setTimeout(() => {
              this.$router.push({ name: "terminated" });
            }, 1000);
          }
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
            var timecount = this.problem.problemset_timeperproblem;
            console.log(this.problem);
            this.timer = setInterval(() => {
              if (
                timecount > 0 &&
                timecount <= this.problem.problemset_timeperproblem
              ) {
                timecount = timecount - 1;
                this.timecountvalue = timecount;
              } else {
                console.log("over");
                console.log("clear timer:", this.timer);
                clearInterval(this.timer);
                this.timer = null;
                this.submitanswer();
              }
            }, 1000);
            console.log("create timer:", this.timer);
            this.$cookie.set("timerid", this.timer);
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
.fixedbar {
  position: fixed;
  top: 0px;
  left: 300px;
  z-index: 999;
  height: 26px;
  text-align: center;
  margin-top: 0px;
  width: 50px;
  color: #f0f0f0;
  font-size: 20px;
  line-height: 26px;
  background-color: #7878a8;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  filter: alpha(Opacity=60);
  -moz-opacity: 0.6;
  opacity: 0.6;
}
.virtualbody {
  width: 100%;
  overflow-y: scroll;
  overflow-x: auto;
}
.changeposition {
  margin-left: 100px;
}
.recoverposition {
  margin-left: 0px;
}
</style>
