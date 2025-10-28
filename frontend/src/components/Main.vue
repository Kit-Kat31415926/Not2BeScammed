<script setup lang="ts">
defineProps<{
  msg: string
}>()


</script>

<template>
  <div class="title">
    <h1 class="green">Not2BeScammed</h1>
    <h3>
      Fish out of water 🐠
    </h3>
  </div>

  <hr>

  <br>
  <br>
  
  <form class="content" @submit.prevent="handleSubmit">
    <label>Enter your email here:</label>
    <textarea class="email-input" />
    <br />
    <button type="submit">
      Submit
    </button>
  </form>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.title h1,
.title h3 {
  text-align: center;
}

.content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.email-input {
  width: 40rem;
  height: 20rem;
}

button {
  border-radius: 7px;
  background-color: lightgreen;
}
</style>
