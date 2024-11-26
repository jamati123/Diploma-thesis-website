<template>
  <div class="account-view">
    <div class="account-header">
      <h1>Willkommen, {{ username || "Benutzer" }}</h1>
      <p class="role">Rolle: <span>{{ role }}</span></p>
    </div>

    <div class="account-info">
      <h2>Deine Kontoinformationen</h2>
      <div class="info-item">
        <strong>E-Mail:</strong> {{ email }}
      </div>
      <div class="info-item">
        <strong>Verbleibende Tokens:</strong> {{ tokens }}
      </div>
      <div class="info-item">
        <strong>Registriert am:</strong> {{ registrationDate || "Unbekannt" }}
      </div>
      <div class="info-item">
        <strong>Letztes Login:</strong> {{ lastLogin || "Unbekannt" }}
      </div>
      <div class="info-item">
        <strong>Verwendete Tokens diesen Monat:</strong> {{ usedTokensThisMonth }}
      </div>
    </div>

    <div class="account-actions">
      <h2>Aktionen</h2>
      <button @click="resetPassword">Passwort zurücksetzen</button>
      <button v-if="role === 'student'" @click="requestStudentPlus">
        Student+ beantragen
      </button>
      <button class="danger" @click="deleteAccount">Account löschen</button>
      <button class="logout" @click="logout">Abmelden</button>
    </div>

    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { getAuth, sendPasswordResetEmail, signOut, deleteUser } from "firebase/auth";
import { getFirestore, doc, getDoc, updateDoc } from "firebase/firestore";

export default {
  data() {
    return {
      email: "",
      tokens: 0,
      username: "",
      role: "",
      registrationDate: "",
      lastLogin: "",
      usedTokensThisMonth: 0,
      successMessage: "",
      errorMessage: "",
    };
  },
  async created() {
    try {
      const auth = getAuth();
      const db = getFirestore();
      const currentUser = auth.currentUser;

      if (currentUser) {
        this.email = currentUser.email;

        const userDoc = await getDoc(doc(db, "users", currentUser.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          this.tokens = data.tokens || 0;
          this.username = data.username || "";
          this.role = data.role || "student";
          this.registrationDate = data.registrationDate || "";
          this.lastLogin = data.lastLogin || "";
          this.usedTokensThisMonth = data.usedTokensThisMonth || 0;
        } else {
          this.errorMessage = "Benutzerdaten nicht gefunden.";
        }
      } else {
        this.errorMessage = "Benutzer ist nicht eingeloggt.";
      }
    } catch (err) {
      this.errorMessage = "Fehler beim Laden der Benutzerdaten: " + err.message;
    }
  },
  methods: {
    async resetPassword() {
      const auth = getAuth();
      try {
        await sendPasswordResetEmail(auth, this.email);
        this.successMessage = "Passwort-Zurücksetzen-E-Mail wurde gesendet.";
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage = "Fehler beim Zurücksetzen des Passworts: " + error.message;
        this.successMessage = "";
      }
    },
    async requestStudentPlus() {
      const db = getFirestore();
      const auth = getAuth();
      const currentUser = auth.currentUser;

      if (currentUser) {
        try {
          const userRef = doc(db, "users", currentUser.uid);
          await updateDoc(userRef, {
            studentPlusRequest: true,
          });
          this.successMessage = "Student+ Beantragung erfolgreich gesendet.";
          this.errorMessage = "";
        } catch (error) {
          this.errorMessage = "Fehler beim Beantragen von Student+: " + error.message;
          this.successMessage = "";
        }
      }
    },
    async deleteAccount() {
      const auth = getAuth();
      try {
        const currentUser = auth.currentUser;
        if (currentUser) {
          await deleteUser(currentUser);
          this.successMessage = "Account erfolgreich gelöscht.";
          this.$router.push("/login");
        }
      } catch (error) {
        this.errorMessage = "Fehler beim Löschen des Accounts: " + error.message;
        this.successMessage = "";
      }
    },
    async logout() {
      const auth = getAuth();
      try {
        await signOut(auth);
        this.$router.push("/login");
      } catch (error) {
        this.errorMessage = "Fehler beim Abmelden: " + error.message;
        this.successMessage = "";
      }
    },
  },
};
</script>

<style scoped>
.account-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.account-header {
  margin-bottom: 20px;
}

.role span {
  font-weight: bold;
  color: #3498db;
}

.account-info {
  text-align: left;
  margin-bottom: 20px;
}

.info-item {
  margin: 10px 0;
  font-size: 1rem;
}

.account-actions button {
  margin: 10px;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.account-actions button:hover {
  background-color: #3498db;
  color: white;
}

button.danger {
  background-color: #e74c3c;
  color: white;
}

button.logout {
  background-color: #95a5a6;
  color: white;
}

.success {
  color: green;
  margin-top: 20px;
}

.error {
  color: red;
  margin-top: 20px;
}
</style>
