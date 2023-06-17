<template>
  <v-app>
    <v-app-bar :elevation="1">
      <v-spacer></v-spacer>
      <span>
        <b>Fluxogramas da UFRJ</b>
      </span>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <slot></slot>
    </v-main>

    <v-footer app border>
      Made by Boechat and BDantas! @{{ new Date().getFullYear() }}
    </v-footer>
  </v-app>
</template>
