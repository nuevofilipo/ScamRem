import type { Handle } from "@sveltejs/kit";
import { auth } from "$lib/firebase";
import { getAuth } from "firebase-admin/auth";
import { redirect } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  const sessionCookie = event.cookies.get("session");

  if (sessionCookie) {
    try {
      const decodedClaims = await getAuth().verifySessionCookie(sessionCookie, true);
      event.locals.user = decodedClaims;
    } catch (error) {
      event.locals.user = null;
    }
  } else {
    event.locals.user = null;
  }

  // redirecting functionality to protect certain routes
  if (event.locals.user && event.url.pathname == "/"){

    console.log("user logged in redirecting to dashboard from hooks.server")
    throw redirect(303, "/dashboard");
  } else if(!event.locals.user && event.url.pathname.startsWith("/dashboard")){
    console.log("user not logged in, redirecting from hooks.server to root")
    throw redirect(303, "/");
  }

  return resolve(event);
};
