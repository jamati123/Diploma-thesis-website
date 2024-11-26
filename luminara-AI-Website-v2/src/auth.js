// src/auth.js
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut} from "firebase/auth";
import { getFirestore, doc, setDoc, getDoc } from "firebase/firestore";
import firebaseApp from "./firebaseConfig";

const auth = getAuth(firebaseApp);
const db = getFirestore(firebaseApp);

export const register = async (email, password) => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  const user = userCredential.user;

  // Initialisiere Tokens und Rolle in Firestore
  await setDoc(doc(db, "users", user.uid), {
    tokens: 100, // Starte mit 100 Tokens
    role: "student", // Standardrolle ist Student
  });

  return user;
};

// Anmelden
export const login = async (email, password) => {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // Lade Tokens aus Firestore
    const userDoc = await getDoc(doc(db, "users", user.uid));
    if (userDoc.exists()) {
      const tokens = userDoc.data().tokens;
      console.log("User Tokens:", tokens);
    } else {
      console.error("No user data found!");
    }

    return user;
  };
// Registrieren
//export const register = async (email, password) => {
//  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
//  return userCredential.user;
//};

// Abmelden
export const logout = async () => {
  await signOut(auth);
};
