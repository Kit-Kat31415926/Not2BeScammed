<template>
	<div class="fun-fact">
		<h3 class="pretty-purple">Did you know?</h3>
		<p class="pretty-blue">Emails are responsible for as much as <i>90%</i> of cyberattacks!</p>
	</div>

	<form class="email-content" @submit.prevent="analyzeEmail">
		<label>Find out if you're the target of a cyberattack. Paste your email below...</label>
		<textarea class="email-input" ref="emailContent" :disabled="inputDisabled" />
		<br />
		<button v-if="!analyzed" class="button" type="submit">
			ANALYZE
		</button>
  	</form>

	<div v-if="analyzed" class="analysis">
		<h3 id="result"><i>Results:</i></h3>
	</div>
</template>

<script>
export default {
	data() {
		return {
			analyzed: false,
			inputDisabled: false,
			aiResult: ""
		}
	},
	methods: {
		analyzeEmail() {
			this.analyzed = true;
			this.inputDisabled = true;

			// Call API to get ML analysis
			this.getAnalysis(this.$refs.emailContent.value);
		},
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
				})
				.catch(error => console.error('Error fetching data:', error));
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