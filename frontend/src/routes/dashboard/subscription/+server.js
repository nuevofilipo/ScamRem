import { json } from "@sveltejs/kit";

export async function POST({ request, cookies }) {

  const body = await request.json();
  console.log("Received body:", JSON.stringify(body));
  const expiresIn = 60 * 60 * 24 * 5 * 1000; // 5 days

  let subscriptionValue = String(body.value);
  console.log(typeof subscriptionValue);

  cookies.set("subscription", JSON.stringify(body), {
    httpOnly: true,
    secure: true,
    maxAge: expiresIn,
    path: "/"
  });

  console.log("successfully set subscription cookie to value: ", body);

  return json({ success: true });
}
