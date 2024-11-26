// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBNLYpEkMqCoTfuADDrJ8i9-sGthNT7k4E",
  authDomain: "diploma-thesis-95db7.firebaseapp.com",
  projectId: "diploma-thesis-95db7",
  storageBucket: "diploma-thesis-95db7.appspot.com",
  messagingSenderId: "777604330607",
  appId: "1:777604330607:web:345508ad50b10e3a64099a",
};
// Firebase initialisieren
const app = initializeApp(firebaseConfig);

// Firebase Auth initialisieren
const auth = getAuth(app);

export { app, auth };