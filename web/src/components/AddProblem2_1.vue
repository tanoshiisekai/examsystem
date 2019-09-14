<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-field>
      <label>添加题库压缩包</label>
      <md-file v-model="filename" @md-change="onFileUpload($event)" />
    </md-field>
    <md-field>
      <label>请输入题库描述</label>
      <md-input v-model="problemsetdesp"></md-input>
    </md-field>
    <md-button class="md-raised md-accent" @click="addProblemSet()">确定</md-button>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
export default {
  name: "addproblem2_1",
  components: {
    AdminMenu
  },
  data() {
    return {
      filename: "",
      fileobj: "",
      problemtitle: "",
      problemsetdesp: "",
      showSnackbar: false,
      message: "",
      uploadurl: ""
    };
  },
  methods: {
    addProblemSet() {
      var token = this.$cookie.get("usertoken");
      this.problemsettitle = this.$cookie.get("problemsettitle");
      this.axios
        .get(
          "/ProblemSet/upload/" +
            token +
            "/" +
            this.problemsettitle +
            "/" +
            this.problemsetdesp
        )
        .then(response => {
          var resp = response.data;
          console.log(resp);
          this.showSnackbar = true;
          this.message = resp["infomsg"];
          setTimeout(() => {
            this.$router.push({ name: "addproblem1" });
          }, 2000);
        });
    },
    onFileUpload(evt) {
      var token = this.$cookie.get("usertoken");
      var formData = new FormData();
      formData.append("file", evt[0]);
      var config = {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      };
      this.axios
        .post("/ProblemSet/upload/" + token, formData, config)
        .then(response => {
          var resp = response.data;
          console.log(resp);
          this.showSnackbar = true;
          this.message = resp["infomsg"];
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
