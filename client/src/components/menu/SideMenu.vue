<template>
  <n-collapse-transition :show="!collapsed">
    <div class="p-2">
      <n-card size="small">
        <div class="d-flex justify-content-center align-items-center flex-column text-center">
          <n-avatar :size="100" circle object-fit="cover" src="https://cataas.com/cat?width=200"/>

          <h3 class="m-0 mt-2">{{ userStore.currentUser?.displayName }}</h3>
        </div>
      </n-card>
    </div>
  </n-collapse-transition>

  <n-menu
      :collapsed-icon-size="22"
      :collapsed-width="64"
      :collapsed="collapsed"
      :value="$route.path.split('/')[1]"
      :options="menuOptionsFiltered"
  />
</template>

<script lang="ts" setup>
import {menuOptions} from "@data/menuData.ts";
import {computed} from "vue";
import {useUserStore} from "@data/store/userStore.ts";

defineProps<{collapsed: boolean}>()

const userStore = useUserStore();

const menuOptionsFiltered = computed(() => {
  return menuOptions.filter((m) => m.roles.includes(userStore.currentUser?.role || ''))
})
</script>

<style scoped>

</style>