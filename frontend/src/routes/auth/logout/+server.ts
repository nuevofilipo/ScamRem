// export const POST = async ({ cookies }) => {
//     cookies.set("session", "", { expires: new Date(0), path: "/" });
//     return new Response(JSON.stringify({ success: true }));
//   };
  
  import { json } from "@sveltejs/kit";

  export function POST({ cookies }) {
    cookies.delete("session", { path: "/" }); // Remove session cookie
  
    return json({ success: true });
  }
  