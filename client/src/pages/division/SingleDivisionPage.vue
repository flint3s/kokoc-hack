<template>
  <div class="content-container">
    <div>
      <h2 v-if="!isLoading" class="text-center">Подразделение {{ companyItem?.title }} / {{ divisionItem?.title }}</h2>
      <n-skeleton v-else text width="100%"/>
    </div>

    <n-scrollbar x-scrollable>
      <div class="scroll-container">
        <n-data-table
            :columns="employeeColumns"
            :data="divisionItem?.employees"
            :loading="isLoading"
            :pagination="{pageSize: 10}"
        />
      </div>
    </n-scrollbar>

    <n-modal :show="isEmployeeManageModalShown" closable>
      <n-card :title="'Управление пользователем ' + selectedEmployee?.name + ' ' + selectedEmployee?.surname"
              class="card-md"
              closable
              @close="isEmployeeManageModalShown = false"
      >
        <n-form-item v-if="selectedEmployee" label="Подразделение">
          <n-select v-model:value="selectedEmployee!.division_id" :options="divisions" label-field="title"
                    value-field="id"/>
        </n-form-item>

        <template #action>
          <n-space>
            <n-button type="primary" @click="onClickSaveEmployee">
              Сохранить
            </n-button>

            <n-button secondary>
              Отменить
            </n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>
  </div>
</template>

<script lang="ts" setup>
import {h, onBeforeMount, ref} from 'vue'
import {useRoute, useRouter} from "vue-router";
import {axiosInstance} from "@data/api/axiosInstance.ts";
import {Company} from "@data/types/company.ts";
import {Division} from "@data/types/division.ts";
import {DataTableColumn, NButton} from "naive-ui";


const route = useRoute()
const router = useRouter()


const companyItem = ref<Company | null>(null)
const divisionItem = ref<Division | null>(null)
const divisions = ref<Division[]>([])

const isLoading = ref(false)

const selectedEmployee = ref<{ user_id: number, id: number, name: string, surname: string, division_id: number } | null>(null)
const isEmployeeManageModalShown = ref(false);

const loadCompany = async () => {
  companyItem.value = (await axiosInstance.get('/companies/get/' + route.params?.companyId)).data as Company
}

const loadDivision = async () => {
  divisionItem.value = (await axiosInstance.get('/divisions/get/' + route.params?.divisionId)).data as Division
}

const loadDivisions = async () => {
  divisions.value = (await axiosInstance.get('/divisions/get-all/' + route.params?.companyId)).data as Division[]
}

const fetchAll = async () => {
  isLoading.value = true
  await Promise.all([loadDivision(), loadCompany(), loadDivisions()])
  isLoading.value = false
}

const onClickSaveEmployee = async () => {
  await axiosInstance.post('/employees/change-division', {employee_id: selectedEmployee.value?.id, division_id: selectedEmployee.value?.division_id})
  await fetchAll()
  isEmployeeManageModalShown.value = false
}

onBeforeMount(async () => {
  await fetchAll()
})

const employeeColumns: DataTableColumn[] = [
  {
    title: '#',
    key: 'index',
    render: (_, i) => {
      return `${i + 1}`
    }
  },
  {
    title: 'Имя',
    key: 'name'
  },
  {
    title: 'Фамилия',
    key: 'surname'
  },
  {
    title: 'Управление',
    key: 'goto',
    render: (row, _) => {
      return h(
          NButton,
          {
            size: 'small',
            onClick: () => {
              selectedEmployee.value = row as { user_id: number; id: number; name: string; surname: string; division_id: number }
              isEmployeeManageModalShown.value = true
            }
          },
          {default: () => 'Управление'}
      )
    }
  },
  {
    title: 'Профиль',
    key: 'goto',
    render: (row, __) => {
      return h(
          NButton,
          {
            size: 'small',
            onClick: () => {
              router.push('/employees/' + row.id)
            }
          },
          {default: () => 'Открыть профиль'}
      )
    }
  }
]
</script>

<style scoped>

</style>