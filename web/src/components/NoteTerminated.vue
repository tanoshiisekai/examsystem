<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">查看错题被中止</span>
    </md-subheader>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
export default {
  name: "noteterminated",
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
