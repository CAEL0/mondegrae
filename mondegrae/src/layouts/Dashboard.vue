<template>
  <div class="leading-normal tracking-normal" id="main-body">
    <div class="flex flex-wrap text-gray-500 dark:text-gray-400">
      <div
        class="w-full bg-gray-200 dark:bg-gray-900"
        id="main-content"
      >
        <div class="min-h bg-gray-200 dark:bg-gray-900">
          <fade-transition>
            <keep-alive include="DashboardHome,Logs,Commands" :max="3">
              <router-view />
            </keep-alive>
          </fade-transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FadeTransition } from "vue2-transitions";

export default {
  name: "Dashboard",
  components: {
    FadeTransition,
  },
};
</script>

<style scoped>
.min-h {
  min-height: calc(100% - 8rem);
}
#main-content {
  padding-top: 5%;
  padding-inline: 20%;
}
</style>