<template>
    <!-- Load logo on front page -->
    <img src="/home_logo.png" width="100%" />
    <!-- Create launch button -->
    <button id="begin" class="button" @click="launch">Fish for Phish! 🎣</button>
</template>

<script>
export default {
    methods: {
        // Navigate to the Analyze tab
        launch() {
            this.$router.push('/analyze');
        }
    }
}
</script>

<style scoped>
img {
    user-select: none;
}

/* Pulsing button */
.button {
    animation:btn 2s;
    -webkit-animation:btn 5s;
    animation-iteration-count:infinite;
    -webkit-animation-iteration-count:infinite;
}

@keyframes btn  {
    0%   {color: white; background-color: #8c52ff; text-shadow:0 0 9px rgba(255,255,144,0);}
    50%  {color: white; background-color: #5ce1e6; text-shadow:0 0 9px rgba(255,255,144,0.75);}
    100% {color: white; background-color: #8c52ff; text-shadow:0 0 9px rgba(255,255,144,0);}
}

@-webkit-keyframes btn {
    0%   {color: white; background-color: #8c52ff; text-shadow:0 0 9px rgba(255,255,144,0);}
    50%  {color: white; background-color: #5ce1e6; text-shadow:0 0 9px rgba(255,255,144,0.75);}
    100% {color: white; background-color: #8c52ff; text-shadow:0 0 9px rgba(255,255,144,0);}
}
</style>
