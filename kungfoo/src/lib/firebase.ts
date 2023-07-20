// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { doc, getFirestore, onSnapshot } from "firebase/firestore";
import { getAuth, onAuthStateChanged, type User } from "firebase/auth";
import { getStorage } from "firebase/storage";
import { writable,type Readable, derived } from "svelte/store";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAsAKigo9bcliPb0XBi5NUT1axmb6ViKDA",
    authDomain: "kunfoo-41db8.firebaseapp.com",
    projectId: "kunfoo-41db8",
    storageBucket: "kunfoo-41db8.appspot.com",
    messagingSenderId: "903101550157",
    appId: "1:903101550157:web:4263703c9a8bf069e91604"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Initialize Firebase
export const db = getFirestore();
export const auth = getAuth();
export const storage = getStorage();


function userStore() {
    let unsubscribe: () => void;
    
    if (!auth || !globalThis.window) {
        console.warn("Auth is not initialized or not in browser");
        const { subscribe} = writable<User | null>(null);
        
    }

    const {subscribe} = writable(auth?.currentUser ?? null, (set) => {
        unsubscribe = onAuthStateChanged(auth, (user) => {
            set(user);
        });
        return () => unsubscribe();
    });

    return {
        subscribe, 
    };
}

export const user = userStore();


export function docStore<T>(
    path:string,
) {
    let unsubscribe: () => void;

    const docRef = doc(db, path);

    const { subscribe } = writable<T | null>(null, (set) => {
        onSnapshot(docRef, (snapshot) => {
            set((snapshot.data() as T) ?? null);
        });

        return () => unsubscribe();
    });

    return {
        subscribe,
        ref: docRef,
        id: docRef.id,
    };
}

interface UserData {
    username: string;
    bio: string;
    photoURL: string;
    links: any[];
}
export const userData: Readable<UserData | null> = derived(user, ($user, set) => {
    if ($user) {
        return docStore<UserData>(`users/${$user.uid}`).subscribe(set);
    } else {
        set(null);
    }
});  