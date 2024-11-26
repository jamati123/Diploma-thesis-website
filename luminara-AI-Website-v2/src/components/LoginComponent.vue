<template>
  <div class="auth-container">
    <h1>Anmelden</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">E-Mail</label>
        <input type="email" id="email" v-model="email" placeholder="E-Mail" required />
      </div>
      <div class="form-group">
        <label for="password">Passwort</label>
        <input type="password" id="password" v-model="password" placeholder="Passwort" required />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? "Anmelden..." : "Anmelden" }}
      </button>
    </form>
    <button @click="handleGoogleLogin" class="google-login-button">
      Mit Google anmelden
    </button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p>Kein Konto? <router-link to="/register">Hier registrieren</router-link>.</p>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { getFirestore, doc, updateDoc, serverTimestamp } from "firebase/firestore";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      const auth = getAuth();
      const db = getFirestore();

      try {
        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password);
        const user = userCredential.user;

        // Letztes Login aktualisieren
        await updateDoc(doc(db, "users", user.uid), {
          lastLogin: serverTimestamp(),
        });

        this.$router.push("/account");
      } catch (error) {
        this.errorMessage = "Anmeldung fehlgeschlagen: " + error.message;
      } finally {
        this.loading = false;
      }
    },
    async handleGoogleLogin() {
      const auth = getAuth();
      const db = getFirestore();
      const provider = new GoogleAuthProvider();

      try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;

        // Letztes Login aktualisieren
        await updateDoc(doc(db, "users", user.uid), {
          lastLogin: serverTimestamp(),
        });

        this.$router.push("/account");
      } catch (error) {
        this.errorMessage = "Google Anmeldung fehlgeschlagen: " + error.message;
      }
    },
  },
};
</script>

<style scoped>
.google-login-button {
  margin-top: 20px;
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100%;
}

.google-login-button:hover {
  background-color: #357ae8;
}
  .auth-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 40px;
    text-align: center;
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
    text-align: left;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    width: 100%;
  }
  
  button:hover {
    background-color: #2980b9;
  }
  
  button:disabled {
    background-color: #ddd;
    cursor: not-allowed;
  }
  
  .error {
    color: red;
    margin-top: 20px;
  }
  </style>
  