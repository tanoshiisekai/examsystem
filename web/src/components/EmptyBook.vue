<template>
  <div class="container">
    <UserMenu></UserMenu>
    <md-subheader>
      <span class="md-title">当前无错题，请先答题</span>
    </md-subheader>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu";
export default {
  name: "emptybook",
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
