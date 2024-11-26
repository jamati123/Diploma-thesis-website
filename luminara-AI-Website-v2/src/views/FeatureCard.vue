<template>
  <div class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:-translate-y-2">
    <div class="text-5xl mb-4 animate-bounce-slow">{{ icon }}</div>
    <h3 class="text-2xl font-semibold mb-2 text-indigo-600">{{ title }}</h3>
    <p class="text-gray-700">{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: 'FeatureCard',
  props: {
    title: String,
    description: String,
    icon: String
  }
}
</script>

<style scoped>
/* Langsame Bounce-Animation für Icons */
@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-bounce-slow {
  animation: bounce-slow 3s infinite;
}

/* Styling für die FeatureCard */
div {
  background: linear-gradient(to bottom right, #f9fafb, #e0e7ff);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  transform-origin: center;
}

/* Hover-Effekt: Schatten und leichte Bewegung */
div:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-8px);
}

/* Icon Styling */
.text-5xl {
  color: #4f46e5;
  text-align: center;
  font-size: 3rem;
}

/* Titel Styling */
.text-2xl {
  color: #4f46e5;
  text-align: center;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

/* Beschreibung Styling */
p {
  color: #4b5563; /* Neutraler Grau-Ton */
  font-size: 1rem;
  line-height: 1.5;
  text-align: center;
}
</style>
