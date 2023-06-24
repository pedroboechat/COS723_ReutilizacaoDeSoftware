<template>
  <v-container>
    <h2>Escolha um curso:</h2>
    <v-autocomplete
      v-if="coursesItems.length > 0"
      v-model="courseSelection"
      placeholder="Selecione um curso para acessar seu fluxograma."
      :items="coursesItems"
      clearable
    >
    </v-autocomplete>
    <v-progress-circular
      v-else
      color="black"
      indeterminate
    ></v-progress-circular>
    <Fluxograma :course="courseSelection" />
  </v-container>
</template>

<script setup lang="ts">
// @ts-nocheck
// type SubjectData = {
//   course: string;
//   semesters: [
//     {
//       id: number;
//       name: string;
//       subjects: [
//         {
//           name: string;
//           code: string;
//           credits: number;
//         }
//       ];
//     }
//   ];
// };

const coursesItems = ref([]);
const courseSelection = ref(null);
async function getAvailableCourses() {
  const coursesItems: string[] = await $fetch(
    "http://localhost:5000/api/courses",
    {
      method: "GET",
    }
  );
  return coursesItems;
}

onMounted(async () => {
  coursesItems.value = await getAvailableCourses();
});
</script>
