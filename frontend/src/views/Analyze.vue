<template>
	<div class="fun-fact">
		<h3 class="pretty-purple">Did you know?</h3>
		<p class="pretty-blue">Emails are responsible for as much as <i>90%</i> of cyberattacks!</p>
	</div>

	<!-- Create form for submitted email content -->
	<form class="email-content" @submit.prevent="analyzeEmail">
		<label>Find out if you're the target of a cyberattack. Paste your email below...</label>
		<textarea class="email-input" ref="emailContent" :disabled="inputDisabled" />
		<br />
		<button v-if="!analyzed" class="button" type="submit">ANALYZE</button>
  	</form>

	<!-- Show results from ML model -->
	<div v-if="analyzed" class="analysis">
		<h3 id="result"><i>Results:</i></h3>
		<p v-if="loading">Analyzing...</p>
		<p v-else>
			This email has a {{ (aiResult * 100).toFixed(2) }}% chance of being spam.
			<span v-if="aiResult >= 0.95">
				<br />
				<br />
				We do not recommend trusting the contents of this message.
			</span>
		</p>

		<button class="button" @click="tryAgain()" style="margin: 5% auto">🔄️ Try Again</button>
	</div>
</template>

<script>
export default {
	data() {
		// Create all state variables
		return {
			analyzed: false,
			inputDisabled: false,
			aiResult: "",
			loading: false
		}
	},
	methods: {
		// Get user input and fetch results from model
		analyzeEmail() {
			this.inputDisabled = true;
			this.analyzed = true;
			this.loading = true;

			// Call API to get ML analysis
			this.getAnalysis(this.$refs.emailContent.value);
		},
		// Create API call for model
		getAnalysis(emailContent) {
			fetch('http://localhost:5000/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(emailContent)
                })
				.then(response => response.json())
				.then(data => {
					this.aiResult = data.data;
					this.loading = false;
				})
				.catch(error => console.error('Error fetching data:', error));
		},
		tryAgain() {
			this.$refs.emailContent.value = "";
			this.inputDisabled = false;
			this.analyzed = false;
		}
	}
}
</script>

<style scoped>
.email-content {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.email-input {
	width: 40rem;
	height: 18rem;
	margin: 1%;
	border-radius: 7px;
	padding: 7px;
}

.analysis {
	text-align: center;
}
</style>
