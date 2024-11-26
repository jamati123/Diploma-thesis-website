<template>
    <div>
      <h1>Token-Verbrauch ChatGPT</h1>
      <p>Verbleibende Tokens: {{ tokens }}</p>
      <button @click="useToken" :disabled="tokens <= 0">
        Token verwenden
      </button>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
    </div>
  </template>
  
  <script>
  import { getAuth } from "firebase/auth";
  import { getFirestore, doc, getDoc, updateDoc } from "firebase/firestore";
  
  export default {
    data() {
      return {
        tokens: 0, // Verfügbare Tokens
        error: "", // Fehlernachricht
        success: "", // Erfolgsnachricht
      };
    },
    async created() {
      try {
        // Firebase Auth und Firestore
        const auth = getAuth();
        const db = getFirestore();
  
        const currentUser = auth.currentUser;
  
        if (currentUser) {
          // Benutzer-Dokument abrufen
          const userDoc = await getDoc(doc(db, "users", currentUser.uid));
          if (userDoc.exists()) {
            this.tokens = userDoc.data().tokens; // Tokens laden
          } else {
            this.error = "Benutzerdaten nicht gefunden.";
          }
        } else {
          this.error = "Benutzer ist nicht eingeloggt.";
        }
      } catch (err) {
        this.error = "Fehler beim Laden der Tokens: " + err.message;
      }
    },
    methods: {
      async useToken() {
        try {
          // Firebase Auth und Firestore
          const auth = getAuth();
          const db = getFirestore();
  
          const currentUser = auth.currentUser;
  
          if (currentUser) {
            const userRef = doc(db, "users", currentUser.uid);
            const userDoc = await getDoc(userRef);
  
            if (userDoc.exists()) {
              const currentTokens = userDoc.data().tokens;
  
              if (currentTokens > 0) {
                // Token verwenden
                await updateDoc(userRef, {
                  tokens: currentTokens - 1,
                });
                this.tokens = currentTokens - 1; // Lokale Anzeige aktualisieren
                this.success = "Token erfolgreich verwendet!";
                this.error = ""; // Fehler zurücksetzen
              } else {
                this.error = "Nicht genug Tokens!";
                this.success = "";
              }
            } else {
              this.error = "Benutzer nicht gefunden.";
              this.success = "";
            }
          } else {
            this.error = "Benutzer ist nicht eingeloggt.";
            this.success = "";
          }
        } catch (err) {
          this.error = "Fehler beim Verwenden des Tokens: " + err.message;
          this.success = "";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .error {
    color: red;
    margin-top: 10px;
  }
  .success {
    color: green;
    margin-top: 10px;
  }
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  