<template>
  <v-container v-if="!!props.course">
    <v-col>
      <v-row justify="center" class="mb-10">
        <v-btn-toggle
          v-model="toggle"
          color="black"
          variant="tonal"
          divided
          mandatory
        >
          <v-btn
            icon="mdi-magnify"
            value="detail"
            @click="selectedColor.value = null"
          ></v-btn>
          <v-btn
            icon="mdi-palette"
            value="paint"
            :color="colors[selectedColor]"
            @click="changeSelectedColor"
          ></v-btn>
        </v-btn-toggle>
      </v-row>
      <v-row>
        <v-col
          v-for="semester in fluxogramaData.semesters"
          :key="semester.id"
          class="flex-grow-0 mr-5"
        >
          <v-row style="margin-bottom: 10px" justify="start">
            <v-card width="200px" color="black">
              <v-card-title style="text-align: center">
                {{ semester.name }}
              </v-card-title>
            </v-card>
          </v-row>
          <v-row
            v-for="subject in semester.subjects"
            :key="subject.code"
            justify="start"
            style="margin-bottom: 10px"
          >
            <v-card
              :id="subject.code"
              :key="subject.code"
              variant="tonal"
              :color="getCoursesColors(subject.code)"
              width="200px"
              height="140px"
              @click.stop="clickAction($event, subject.code)"
            >
              <v-card-title style="text-align: center">
                {{ subject.code }}
              </v-card-title>
              <v-card-item style="text-align: center; padding: 8px">
                {{ subject.name }}
              </v-card-item>
            </v-card>
          </v-row>
        </v-col>
      </v-row>
    </v-col>
  </v-container>
</template>

<script setup lang="ts">
// @ts-nocheck
// Tipagem do JSON das matérias de um curso
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

const fluxogramaData = ref(null);
const toggle = ref("detail");
const colors = [
  "#b7ff59",
  "#cb87ff",
  "#59ffe6",
  "#ff5959",
  "#ff9e59",
  "#ffee59",
  "#5659fc",
  "#ff19d5",
  "#000000",
];
const selectedColor = ref(null);
const coursesColors = ref({});

// Props do componente
const props = defineProps({
  course: {
    type: String,
    default: "",
  },
});

// Função para mudar a cor
function changeSelectedColor() {
  if (selectedColor.value === null) {
    selectedColor.value = 0;
  } else if (selectedColor.value === colors.length - 1) {
    selectedColor.value = 0;
  } else {
    selectedColor.value++;
  }
}

function getCoursesColors(code) {
  const colorId = coursesColors.value[code];
  if (colorId === undefined || colorId === null) {
    return null;
  }
  return colors[colorId];
}

// const getCoursesColors = computed((x) => colors[x]);

function clickAction(_event, code) {
  if (toggle.value === "detail") {
    console.log("Detail");
  } else if (toggle.value === "paint") {
    coursesColors.value[code] =
      coursesColors.value[code] === selectedColor.value
        ? null
        : selectedColor.value;
  }
}

// Lógica para pegar dados da matéria pela API
async function getCourseFluxograma(course: string) {
  if (course === null) {
    return { semesters: [] };
  }
  const fluxogramaData = await $fetch("http://localhost:5000/api/courses", {
    method: "POST",
    body: {
      course,
    },
  });
  return fluxogramaData;
}

watch(
  () => props.course,
  async (newCourse) => {
    fluxogramaData.value = await getCourseFluxograma(newCourse);
  },
  { immediate: true }
);
</script>

<style scoped>
.foo {
  color: aliceblue;
}
</style>
