<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">答题</span>
    </md-subheader>
    <md-field>
      <label>请输入题库名称</label>
      <md-input v-model="problemsettitle"></md-input>
    </md-field>
    <md-button class="md-raised md-primary" @click="onbegin()">开始答题</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "problems",
  components: {
    UserMenu
  },
  created() {
    var timerid = this.$cookie.get("timerid");
    clearInterval(timerid);
  },
  data() {
    return {
      problemsettitle: "",
      showSnackbar: false,
      message: ""
    };
  },
  methods: {
    onbegin() {
      if (this.problemsettitle.length == 0) {
        this.message = "题库名称不能为空!";
      } else {
        var usertoken = this.$cookie.get("usertoken");
        this.$cookie.set("problemsettitle", this.problemsettitle);
        this.axios
          .get("/ProblemSet"+apiversion+"/" + usertoken + "/" + this.problemsettitle)
          .then(response => {
            var resp = response.data;
            console.log(resp);
            if (resp["infostatus"] == 1) {
              this.message = "题库获取成功!";
              setTimeout(() => {
                this.$router.push({ name: "answerproblems" });
              }, 1000);
            } else {
              this.message = resp["infomsg"];
            }
          });
      }
      this.showSnackbar = true;
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
