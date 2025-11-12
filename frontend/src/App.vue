<template>
    <div class="wrapper">
		<!-- Create navigation bar -->
		<nav v-if="route.path != '/'" class="nav-bar">
			<RouterLink class="pretty-purple" to="/analyze">Analyze</RouterLink>
			<RouterLink class="pretty-purple" to="/simulate">Simulate</RouterLink>
			<RouterLink class="pretty-purple" to="/about">About</RouterLink>
		</nav>
		<!-- Render component based on router -->
		<main>
			<RouterView />
		</main>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();

const isHome = () => {
	return route.path == '/';
};
</script>

<style>
.nav-bar {
	margin-bottom: 3%;
}

.nav-bar * {
	font-size: medium;
	margin-right: 3%;
}
</style>