<template>
  <div class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:-translate-y-2 flex-1">
    <div class="text-5xl mb-4">{{ icon }}</div>
    <h3 class="text-2xl font-semibold mb-2 text-indigo-600">{{ title }}</h3>
    <p class="text-gray-700">{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: 'AccountCard',
  props: {
    title: String,
    description: String,
    icon: String
  }
}
</script>

<style scoped>
/* Styling für die AccountCard */
div {
  background: linear-gradient(to bottom right, #ffffff, #eef2ff);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform-origin: center;
}

/* Hover-Effekt */
div:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-8px);
  background: linear-gradient(to bottom right, #f0f4ff, #dfe7fd);
}

/* Icon Styling */
.text-5xl {
  color: #4f46e5;
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
}

/* Titel Styling */
.text-2xl {
  color: #4f46e5;
  font-weight: 600;
  margin-bottom: 0.75rem;
  text-align: center;
}

/* Beschreibung Styling */
p {
  color: #374151; /* Neutraler Dunkelgrau-Ton */
  font-size: 1rem;
  line-height: 1.5;
  text-align: center;
}
</style>
