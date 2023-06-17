<template>
  <v-container v-if="!!props.course">
    <v-col>
      <v-row justify="center" class="mb-5">
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
          <v-row style="margin-bottom: 5px" justify="start">
            <v-card width="120px" color="black">
              <v-card-title style="text-align: center; font-size: 16px;">
                {{ semester.name }}
              </v-card-title>
            </v-card>
          </v-row>
          <v-row
            v-for="subject in semester.subjects"
            :key="subject.code"
            justify="start"
            style="margin-bottom: 5px"
          >
            <v-card
              :id="subject.code"
              :key="subject.code"
              :color="getCoursesColors(subject.code)"
              width="120px"
              height="120px"
              @click.stop="clickAction($event, subject)"
            >
              <v-card-title style="text-align: center; color: black !important; font-size: 14px;">
                {{ subject.code }}
              </v-card-title>
              <v-card-item
                style="
                  text-align: center;
                  padding: 8px;
                  color: black !important;
                  font-size: 12px;
                "
              >
                {{ subject.name }}
              </v-card-item>
            </v-card>
          </v-row>
        </v-col>
      </v-row>
    </v-col>
    <v-overlay :model-value="overlay" class="align-center justify-center">
      <v-col>
        <v-row>
          <v-card style="height: 500px; width: 500px">
            <v-card-title>
              {{ overlayTitle }}
            </v-card-title>
            <v-card-item>
              <b>Ementa:</b>
              <p>{{ overlayEmenta }}</p>
              <br />
              <b>Último semestre oferecida:</b>
              <p>{{ overlayUltimoSemestre }}</p>
              <br />
              <b>Requisitos:</b>
              <p>{{ overlayRequisitos }}</p>
            </v-card-item>
          </v-card>
        </v-row>
      </v-col>
    </v-overlay>
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
];
const selectedColor = ref(null);
const coursesColors = ref({});
const overlay = ref(false);
const overlayTitle = ref("");
const overlayEmenta = ref("");
const overlayUltimoSemestre = ref("");
const overlayRequisitos = ref("");

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

function clickAction(_event, subject) {
  if (toggle.value === "detail") {
    overlayTitle.value = `${subject.code} - ${subject.name}`;
    overlayEmenta.value = `Ementa para a matéria ${subject.name}.`;
    overlayUltimoSemestre.value = `2022/2 - ${subject.name}`;
    overlayRequisitos.value = `Requisitos da matéria ${subject.name}`;
    overlay.value = !overlay.value;
  } else if (toggle.value === "paint") {
    coursesColors.value[subject.code] =
      coursesColors.value[subject.code] === selectedColor.value
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
