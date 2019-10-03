<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <md-button class="md-primary" @click="gettemplate()">下载题库模板</md-button>
    </md-subheader>
    <md-field>
      <label>请输入题库名称</label>
      <md-input v-model="problemsettitle"></md-input>
    </md-field>
    <md-button class="md-raised md-primary" @click="onnext()">继续</md-button>
    <md-dialog :md-active.sync="showDialog1">
      <md-dialog-title>提示</md-dialog-title>
      <md-card-content>题库已存在，确定继续添加题目吗？</md-card-content>
      <md-dialog-actions>
        <md-button class="md-primary mybutton" @click="addproblem1()">是</md-button>
        <md-button class="md-primary mybutton" @click="showDialog1 = false">否</md-button>
      </md-dialog-actions>
    </md-dialog>
    <md-dialog :md-active.sync="showDialog2">
      <md-dialog-title>提示</md-dialog-title>
      <md-card-content>题库不存在，确定新建题库吗？</md-card-content>
      <md-dialog-actions>
        <md-button class="md-primary mybutton" @click="addproblem2()">是</md-button>
        <md-button class="md-primary mybutton" @click="showDialog2 = false">否</md-button>
      </md-dialog-actions>
    </md-dialog>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
import { filehost, fileport } from "@/conf";
export default {
  name: "addproblem1",
  components: {
    AdminMenu
  },
  data() {
    return {
      problemsettitle: "",
      showDialog1: false,
      showDialog2: false
    };
  },
  methods: {
    gettemplate() {
      var fileurl = "http://" + filehost + ":" + fileport + "/gettemplate/";
      console.log(fileurl);
      window.location.href = fileurl;
    },
    addproblem1() {
      this.showDialog1 = false;
      this.$router.push({ name: "addproblem2_2" });
    },
    addproblem2() {
      this.showDialog2 = false;
      this.$router.push({ name: "addproblem2_1" });
    },
    onnext() {
      var usertoken = this.$cookie.get("usertoken");
      this.$cookie.set("problemsettitle", this.problemsettitle);
      this.axios
        .get("/ProblemSet/" + usertoken + "/" + this.problemsettitle)
        .then(response => {
          var resp = response.data;
          console.log(resp);
          if (resp["infostatus"] == 1) {
            this.showDialog1 = true;
          } else if (resp["infostatus"] == 0) {
            this.showDialog2 = true;
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
