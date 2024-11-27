<!-- src/components/ApplicationDetails.vue -->
<template>
    <div class="application-details">
      <header class="header">
        <h1>Antragsdetails</h1>
      </header>
  
      <section class="details-section">
        <div class="detail-item">
          <strong>Username:</strong>
          <p>{{ application.username }}</p>
        </div>
        <div class="detail-item">
          <strong>E-Mail:</strong>
          <p>{{ application.email }}</p>
        </div>
        <div class="detail-item">
          <strong>Antragsdatum:</strong>
          <p>{{ formatDate(application.requestDate) }}</p>
        </div>
        <div class="detail-item">
          <strong>Status:</strong>
          <p>{{ application.status }}</p>
        </div>
        <div v-if="application.status !== 'pending'" class="detail-item">
          <strong>Bearbeitet am:</strong>
          <p>{{ formatDate(application.reviewDate) }}</p>
        </div>
        <div v-if="application.status !== 'pending'" class="detail-item">
          <strong>Bearbeitet von:</strong>
          <p>{{ application.reviewedBy }}</p>
        </div>
      </section>
  
      <button @click="$router.back()" class="back-button">Zurück</button>
  
      <!-- Erfolg- und Fehlermeldungen -->
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import { getFirestore, doc, getDoc } from "firebase/firestore";
  
  export default {
    data() {
      return {
        application: null,
        successMessage: "",
        errorMessage: "",
      };
    },
    methods: {
      formatDate(timestamp) {
        if (!timestamp) return "Unbekannt";
        return new Intl.DateTimeFormat("de-DE", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        }).format(timestamp.toDate());
      },
      async fetchApplication() {
        const db = getFirestore();
        const applicationId = this.$route.params.id;
        const applicationRef = doc(db, "applications", applicationId);
  
        try {
          const docSnap = await getDoc(applicationRef);
          if (docSnap.exists()) {
            this.application = { id: docSnap.id, ...docSnap.data() };
          } else {
            this.errorMessage = "Antrag nicht gefunden.";
          }
        } catch (error) {
          this.errorMessage = "Fehler beim Laden des Antrags: " + error.message;
        }
      }
    },
    async created() {
      await this.fetchApplication();
    }
  };
  </script>
  
  <style scoped>
  .application-details {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    background: #ffffff;
    border-radius: 15px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    font-family: Arial, sans-serif;
  }
  
  .header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .header h1 {
    font-size: 2.5rem;
    margin: 0;
  }
  
  .details-section {
    margin-bottom: 30px;
  }
  
  .detail-item {
    margin-bottom: 15px;
  }
  
  .detail-item strong {
    display: inline-block;
    width: 150px;
    color: #333;
  }
  
  .back-button {
    background-color: #3498db;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .back-button:hover {
    background-color: #2980b9;
  }
  
  .success {
    color: green;
    text-align: center;
    margin-top: 20px;
  }
  
  .error {
    color: red;
    text-align: center;
    margin-top: 20px;
  }
  </style>
  