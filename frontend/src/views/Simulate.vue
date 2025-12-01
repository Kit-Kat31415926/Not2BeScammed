<template>
    <h3>
        Simulate a spam attack on our ML model, Fisher! Watch Fisher sort through 
        their mail and see how accurate their judgement is as they try not to be scammed.
    </h3>
    <br />
    <form @submit.prevent="startSimulation">
        <div>
            <label for="ham">How many <i>legitimate</i> emails do you want to send to Fisher?</label>
            <br />
            <input required name="ham" ref="numHam" type="number" step="1" min="0" max="50000" />
        </div>
        <br />
        <div>
            <label for="spam">How many <i>scam</i> emails do you want to send to Fisher?</label>
            <br />
            <input required name="spam" ref="numSpam" type="number" step="1" min="0" max="50000" />
        </div>
        <div style="width: fit-content; margin: 1rem;">
            <button :disabled="loading" class="button" style="padding: 0px 1rem;" type="submit">ᯓ➤</button>
        </div>
    </form>
    
    <div style="width: 100%">
        <h4 style="font-weight: bold; text-align: center;">
            {{result}}
        </h4>
    </div>
  <div ref="threeContainer" class="three-scene"></div>
</template>




<script setup>
// Import three.js libraries
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { FontLoader } from 'three/addons/loaders/FontLoader.js'; 
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';
// Import font
import typefaceData from "@compai/font-lora/data/typefaces/normal-400.json";
// Import vue-specific functions
import { onMounted, ref } from 'vue';

var loading = false;
var result = ref("");
const numSpam = ref(null);
const numHam = ref(null);

// Create a reference to the Vue div containing the three.js animations
const threeContainer = ref(null);

// Create variables for the scene
let scene, camera, renderer, mixer, clock, model, scamTextMesh, hamTextMesh;
clock = new THREE.Clock();

// Define speed and rotation of the cute robot Fisher
const maxRotationAngle = THREE.MathUtils.degToRad(45);
const rotationSpeed = 0.001; 

// Function for the animation loop
const animate = () => {
	// Infinitely play the animation
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    if (mixer) {
        mixer.update(delta);
    }

	if (model) {
		// Calculate amount to rotate
		const time = Date.now() * rotationSpeed;
		const oscillation = Math.sin(time);
        if (loading) {
		    model.rotation.y = oscillation * maxRotationAngle;
        }
	}
    
    // Animate the textMeshes to float up and down smoothly
    if (loading) {
        scamTextMesh.position.y = 0.25 + Math.sin(Date.now() * 0.001) * 0.2; 
        hamTextMesh.position.y = 0.25 - Math.sin(Date.now() * 0.001) * 0.2; 
    }

	// Render scene
    renderer.render(scene, camera);
};

// Initialize the Three.js scene
const initThree = () => {
	// Ensure that Vue component to render it exists
    if (!threeContainer.value) return;

    // Setup scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff); 

    camera = new THREE.PerspectiveCamera(75, threeContainer.value.clientWidth / threeContainer.value.clientHeight, 0.1, 1000);
    camera.position.set(0, 0.25, 2); 

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight);

    threeContainer.value.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 2);
    scene.add(ambientLight);
	
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // Load cute robot Fisher!
	// Credits to https://sketchfab.com/3d-models/cute-robot-companion-glb-0f64197efce74fba8145b941efea323a
    const loader = new GLTFLoader();
    loader.load(
        '/fisher/source/fisher.glb', 
        (gltf) => {
            model = gltf.scene;
            scene.add(model);
        }, undefined, (error) => {
            console.error('An error occurred while loading the model:', error);
        }
    );

    // Add floating text
    const font = new FontLoader().parse(typefaceData);
    
    // Create the TextGeometry (3D)
    const scamTextGeometry = new TextGeometry('SCAM', {
		font: font, 
		size: 0.1,
		height: 0.02,
		depth: 0.02,
		curveSegments: 12,
		bevelEnabled: false
    });
    const hamTextGeometry = new TextGeometry('HAM', {
		font: font, 
		size: 0.1,
		height: 0.02,
		depth: 0.02,
		curveSegments: 12,
		bevelEnabled: false
    });

    // Create material and mesh
    const scamTextMaterial = new THREE.MeshPhongMaterial({ color: 0xaa3333 });
    scamTextMesh = new THREE.Mesh(scamTextGeometry, scamTextMaterial);
    scamTextMesh.position.set(-0.5, 0, 1.5); // Initial position
    const hamTextMaterial = new THREE.MeshPhongMaterial({ color: 0x33aa33 });
    hamTextMesh = new THREE.Mesh(hamTextGeometry, hamTextMaterial);
    hamTextMesh.position.set(0.1, 0, 1.5); // Initial position

    // Add to scene for display
    scene.add(scamTextMesh);
    scene.add(hamTextMesh);
    
    renderer.render(scene, camera);
};


// Wait until the component is mounted to create the scene and start animation
onMounted(() => {
    initThree();
    animate();
});

const startSimulation = () => {
    loading = true;
    result.value = "Loading...";

    // Get values and pass to endpoint
    let numSpamVal = numSpam.value.value;
    let numHamVal = numHam.value.value;

    fetch('http://localhost:5000/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "spam": numSpamVal, "ham": numHamVal })
        })
        .then(response => response.json())
        .then(data => {
            result.value = data.accuracy;
            loading = false;
        })
        .catch(error => console.error('Error fetching data:', error));
}
</script>

<style scoped>
/* 5. Style the container using its class or ref for specific sizing */
.three-scene {
  width: 100%;
  height: 400px; /* Set a specific height for the canvas */
  background-color: #eee;
}
</style>