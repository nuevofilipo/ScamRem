import { json } from "@sveltejs/kit";
import { adminAuth } from "$lib/server/firebase-admin";

export async function POST({ request, cookies }) {
  const { idToken } = await request.json();

  const expiresIn = 60 * 60 * 24 * 5 * 1000; // 5 days
  const sessionCookie = await adminAuth.createSessionCookie(idToken, { expiresIn });

  cookies.set("session", sessionCookie, {
    httpOnly: true,
    secure: true,
    maxAge: expiresIn,
    path: "/"
  });

  return json({ success: true });
}
