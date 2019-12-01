<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">答题被中止</span>
    </md-subheader>
  </div>
</template>

<script>
  import { filehost, fileport, apiversion } from "@/conf";
import UserMenu from "@/components/UserMenu";
export default {
  name: "terminated",
  components: {
    UserMenu
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
