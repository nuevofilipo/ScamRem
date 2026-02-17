import admin from "firebase-admin";
import { getApps, cert } from "firebase-admin/app";
import { FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY } from "$env/static/private";

if (!getApps().length) {
  admin.initializeApp({
    credential: cert({
      projectId: FIREBASE_PROJECT_ID,
      clientEmail: FIREBASE_CLIENT_EMAIL,
      privateKey: FIREBASE_PRIVATE_KEY.replace(/\\n/g, "\n"),
    }),
  });
}

export const adminAuth = admin.auth();
