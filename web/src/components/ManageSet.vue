<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">题库管理</span>
    </md-subheader>
    <md-table>
      <md-table-row>
        <md-table-head style="text-align:center;">题库名称</md-table-head>
        <md-table-head style="text-align:center;">题库描述</md-table-head>
        <md-table-head style="text-align:center;">题目总数</md-table-head>
        <md-table-head style="text-align:center;">答题数目</md-table-head>
        <md-table-head style="text-align:center;">答题时间</md-table-head>
        <md-table-head style="text-align:center;">操作</md-table-head>
      </md-table-row>

      <md-table-row v-for="dt in datalist" :key="dt.problemset_title">
        <md-table-cell style="text-align:center;">{{dt.problemset_title}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.problemset_desp}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.problemset_count}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.problemset_answercount}}</md-table-cell>
        <md-table-cell style="text-align:center;">{{dt.problemset_timeperproblem}}</md-table-cell>
        <md-table-cell style="text-align:center;">
          <md-button class="md-raised md-accent" @click="handleDelete(dt.problemset_title)">删除</md-button>
          <md-button class="md-raised md-primary" @click="handleSetting(dt.problemset_title)">设置答题数目</md-button>
          <md-button class="md-raised md-primary" @click="handleTime(dt.problemset_title)">设置答题时间</md-button>
          <md-button class="md-raised md-primary" @click="handleCopy(dt.problemset_title)">复制题库</md-button>
        </md-table-cell>
      </md-table-row>
    </md-table>
    <md-dialog :md-active.sync="showDialogAnserCount">
      <md-dialog-title>设置</md-dialog-title>
      <md-field>
        <label>设置答题数目（道）（注意不要少于3道题）</label>
        <md-input v-model="answercount"></md-input>
      </md-field>
      <md-dialog-actions>
        <md-button class="md-primary mybutton" @click="setanswercount()">是</md-button>
        <md-button class="md-primary mybutton" @click="showDialogAnserCount = false">否</md-button>
      </md-dialog-actions>
    </md-dialog>
    <md-dialog :md-active.sync="showDialogAnserTime">
      <md-dialog-title>设置</md-dialog-title>
      <md-field>
        <label>设置答题时间（秒）</label>
        <md-input v-model="answertime"></md-input>
      </md-field>
      <md-dialog-actions>
        <md-button class="md-primary mybutton" @click="setanswertime()">是</md-button>
        <md-button class="md-primary mybutton" @click="showDialogAnserTime = false">否</md-button>
      </md-dialog-actions>
    </md-dialog>
    <md-dialog :md-active.sync="showDialogAnserCopy">
      <md-dialog-title>设置</md-dialog-title>
      <md-field>
        <label>设置新题库的名称</label>
        <md-input v-model="answercopy"></md-input>
      </md-field>
      <md-dialog-actions>
        <md-button class="md-primary mybutton" @click="setanswercopy()">是</md-button>
        <md-button class="md-primary mybutton" @click="showDialogAnserCopy = false">否</md-button>
      </md-dialog-actions>
    </md-dialog>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
  import { filehost, fileport, apiversion } from "@/conf";
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
      datalist: [],
      showDialogAnserCount: false,
      showDialogAnserTime: false,
      showDialogAnserCopy: false,
      answercount: 0,
      answertime: 0,
      answercopy: "",
      dialogsettitle: "",
      showSnackbar: false,
      message: ""
    };
  },
  methods: {
    getdatas() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios.get("/ProblemSet"+apiversion+"/" + usertoken).then(response => {
        var resp = response.data;
        if (resp["infostatus"] == 1) {
          this.datalist = resp["inforesult"];
        } else {
          alert(resp["infomsg"]);
        }
        console.log(this.datalist);
      });
    },
    setanswercount() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get(
          "/ProblemSet"+apiversion+"/setting/" +
            usertoken +
            "/" +
            this.dialogsettitle +
            "/" +
            this.answercount
        )
        .then(response => {
          var resp = response.data;
          console.log(resp);
          this.showDialogAnserCount = false;
          this.showSnackbar = true;
          this.message = resp["infomsg"];
          location.reload();
        });
    },
    setanswertime() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get(
          "/ProblemSet"+apiversion+"/setting1/" +
            usertoken +
            "/" +
            this.dialogsettitle +
            "/" +
            this.answertime
        )
        .then(response => {
          var resp = response.data;
          console.log(resp);
          this.showDialogAnserCount = false;
          this.showSnackbar = true;
          this.message = resp["infomsg"];
          location.reload();
        });
    },
    setanswercopy() {
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get(
          "/ProblemSet"+apiversion+"/copyset/" +
            usertoken +
            "/" +
            this.dialogsettitle +
            "/" +
            this.answercopy
        )
        .then(response => {
          var resp = response.data;
          this.showSnackbar = true;
          this.message = resp["infomsg"];
          location.reload();
        });
    },
    handleDelete(problemsettitle) {
      var usertoken = this.$cookie.get("usertoken");
      this.axios
        .get("/ProblemSet"+apiversion+"/remove/" + usertoken + "/" + problemsettitle)
        .then(response => {
          var resp = response.data;
          if (resp["infostatus"] == 1) {
            location.reload();
          }
        });
    },
    handleSetting(problemsettitle) {
      this.dialogsettitle = problemsettitle;
      this.showDialogAnserCount = true;
    },
    handleTime(problemsettitle) {
      this.dialogsettitle = problemsettitle;
      this.showDialogAnserTime = true;
    },
    handleCopy(problemsettitle) {
      this.dialogsettitle = problemsettitle;
      this.showDialogAnserCopy = true;
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
