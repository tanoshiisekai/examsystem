<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">控制面板</span>
    </md-subheader>
    <md-content>
      <md-switch v-model="switchnotebook" @change="changenotebook()">切换用户错题本功能</md-switch>
    </md-content>
    <md-snackbar :md-duration="3000" :md-active.sync="showSnackbar" md-persistent>
      <span>{{message}}</span>
    </md-snackbar>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
export default {
  name: "controlpanel",
  components: {
    AdminMenu
  },
  created() {
    var admintoken = this.$cookie.get("usertoken");
    this.axios
      .get("/ProblemSet/getnotebooktoggle/" + admintoken)
      .then(response => {
        var resp = response.data;
        console.log(resp);
        if(resp["infostatus"] == 1){
          if(resp["inforesult"] == "1"){
            this.switchnotebook = true;
          }else{
            this.switchnotebook = false;
          }
        }
      });
  },
  data() {
    return {
      message: "",
      showSnackbar: false,
      switchnotebook: true
    };
  },
  methods: {
    changenotebook() {
      if (this.switchnotebook == true) {
        var admintoken = this.$cookie.get("usertoken");
        this.axios
          .get("/ProblemSet/togglenotebookopen/" + admintoken)
          .then(response => {
            var resp = response.data;
            console.log(resp);
          });
      } else {
        var admintoken = this.$cookie.get("usertoken");
        this.axios
          .get("/ProblemSet/togglenotebookclose/" + admintoken)
          .then(response => {
            var resp = response.data;
            console.log(resp);
          });
      }
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
