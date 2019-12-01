<template>
  <div class="container">
    <AdminMenu></AdminMenu>
    <md-subheader>
      <span class="md-title">当前无错题</span>
    </md-subheader>
  </div>
</template>

<script>
import AdminMenu from "@/components/AdminMenu";
  import { filehost, fileport, apiversion } from "@/conf";
export default {
  name: "adminemptybook",
  components: {
    AdminMenu
  },
  created() {
  },
  data() {
    return {
      
    };
  },
  methods: {

  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
