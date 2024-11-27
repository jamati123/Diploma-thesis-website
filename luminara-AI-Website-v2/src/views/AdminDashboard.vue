<template>
    <div class="admin-dashboard">
      <!-- Header -->
      <header class="header">
        <h1>Admin Dashboard</h1>
        <p>Verfügbare Funktionen zur Verwaltung von Student+ Anträgen.</p>
      </header>
  
      <!-- Anträge Liste -->
      <section class="applications-section">
        <h2>Student+ Anträge</h2>
        <table class="applications-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>E-Mail</th>
              <th>Antragsdatum</th>
              <th>Status</th>
              <th>Aktionen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="application in applications" :key="application.id">
              <td>{{ application.username }}</td>
              <td>{{ application.email }}</td>
              <td>{{ formatDate(application.requestDate) }}</td>
              <td>{{ application.status }}</td>
              <td>
                <button 
                  v-if="application.status === 'pending'"
                  @click="approveApplication(application.id)"
                  class="approve-button"
                >
                  Genehmigen
                </button>
                <button 
                  v-if="application.status === 'pending'"
                  @click="rejectApplication(application.id)"
                  class="reject-button"
                >
                  Ablehnen
                </button>
                <button 
                  v-else 
                  @click="viewApplicationDetails(application.id)"
                  class="details-button"
                >
                  Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <!-- Keine Anträge -->
        <p v-if="applications.length === 0">Keine Anträge vorhanden.</p>
      </section>
  
      <!-- Erfolg- und Fehlermeldungen -->
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import { getFirestore, collection, query, where, onSnapshot, updateDoc, doc, getDoc } from "firebase/firestore";
  import { getAuth } from "firebase/auth";
  
  export default {
    data() {
      return {
        applications: [],
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
      async approveApplication(applicationId) {
        const db = getFirestore();
        const auth = getAuth();
        const adminUid = auth.currentUser.uid;
  
        const applicationRef = doc(db, "applications", applicationId);
  
        try {
          await updateDoc(applicationRef, {
            status: "approved",
            reviewDate: new Date(),
            reviewedBy: adminUid,
          });
          this.successMessage = "Antrag erfolgreich genehmigt.";
          this.errorMessage = "";
        } catch (error) {
          this.errorMessage = "Fehler beim Genehmigen des Antrags: " + error.message;
          this.successMessage = "";
        }
      },
      async rejectApplication(applicationId) {
        const db = getFirestore();
        const auth = getAuth();
        const adminUid = auth.currentUser.uid;
  
        const applicationRef = doc(db, "applications", applicationId);
  
        try {
          await updateDoc(applicationRef, {
            status: "rejected",
            reviewDate: new Date(),
            reviewedBy: adminUid,
          });
          this.successMessage = "Antrag erfolgreich abgelehnt.";
          this.errorMessage = "";
        } catch (error) {
          this.errorMessage = "Fehler beim Ablehnen des Antrags: " + error.message;
          this.successMessage = "";
        }
      },
      viewApplicationDetails(applicationId) {
        // Hier kannst du eine Detailansicht öffnen, z.B. ein Modal oder eine neue Route
        this.$router.push(`/admin/applications/${applicationId}`);
      },
      listenToApplications() {
        const db = getFirestore();
        const q = query(collection(db, "applications"), where("status", "==", "pending"));
  
        onSnapshot(q, (querySnapshot) => {
          const apps = [];
          querySnapshot.forEach((doc) => {
            apps.push({ id: doc.id, ...doc.data() });
          });
          this.applications = apps;
        }, (error) => {
          this.errorMessage = "Fehler beim Laden der Anträge: " + error.message;
        });
      }
    },
    async created() {
      const auth = getAuth();
      const currentUser = auth.currentUser;
  
      if (currentUser) {
        // Überprüfen, ob der Benutzer ein Admin ist
        const db = getFirestore();
        const userRef = doc(db, "users", currentUser.uid);
  
        try {
          const docSnap = await getDoc(userRef); // Verwenden Sie getDoc statt userRef.get()
          if (docSnap.exists()) {
            const userData = docSnap.data();
            if (userData.role === "admin") {
              this.listenToApplications();
            } else {
              this.errorMessage = "Zugriff verweigert. Nur Admins können diese Seite sehen.";
              // Weiterleitung zu einer anderen Seite, z.B. Account-Dashboard
              this.$router.push("/account");
            }
          } else {
            this.errorMessage = "Benutzerdaten nicht gefunden.";
          }
        } catch (error) {
          this.errorMessage = "Fehler beim Überprüfen der Benutzerrolle: " + error.message;
        }
      } else {
        this.errorMessage = "Benutzer ist nicht eingeloggt.";
        this.$router.push("/login");
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-dashboard {
    max-width: 1200px;
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
  
  .header p {
    font-size: 1.2rem;
    color: #555;
  }
  
  .applications-section {
    margin-top: 20px;
  }
  
  .applications-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .applications-table th,
  .applications-table td {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: left;
  }
  
  .applications-table th {
    background-color: #f4f4f4;
  }
  
  .applications-table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .applications-table tr:hover {
    background-color: #f1f1f1;
  }
  
  .approve-button {
    background-color: #28a745; /* Grün */
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    margin-right: 5px;
    transition: background-color 0.3s;
  }
  
  .approve-button:hover {
    background-color: #218838;
  }
  
  .reject-button {
    background-color: #dc3545; /* Rot */
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .reject-button:hover {
    background-color: #c82333;
  }
  
  .details-button {
    background-color: #17a2b8; /* Blau */
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .details-button:hover {
    background-color: #138496;
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
  