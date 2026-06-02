// import { NextRequest, NextResponse } from "next/server";
// import { createClient } from "@supabase/supabase-js";

// // Supabase Admin client (serveur)
// const supabaseAdmin = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!, // ← on utilise celle qui existe dans .env
//   process.env.SUPABASE_SERVICE_ROLE_KEY! // clé admin pour supprimer les users
// );

// export async function POST(req: NextRequest) {
//   try {
//     const { userId } = await req.json();

//     if (!userId) {
//       return NextResponse.json({ error: "Missing userId" }, { status: 400 });
//     }

//     // suppression de l'utilisateur
//     const { error } = await supabaseAdmin.auth.admin.deleteUser(userId);

//     if (error) {
//       return NextResponse.json({ error: error.message }, { status: 400 });
//     }

//     return NextResponse.json({ message: "User deleted successfully" });

//   } catch (err) {
//     console.error("Delete account error:", err);
//     return NextResponse.json({ error: "Internal server error" }, { status: 500 });
//   }
// }

import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(req: NextRequest) {
  try {
    const { userId } = await req.json();

    if (!userId) {
      return NextResponse.json(
        { error: "Missing userId" },
        { status: 400 }
      );
    }

    // =========================
    // DELETE RELATED DATA
    // =========================

    const { error: paymentsError } = await supabaseAdmin
      .from("payments")
      .delete()
      .eq("user_id", userId);

    if (paymentsError) {
      console.error("Payments delete error:", paymentsError);
      return NextResponse.json(
        { error: "Failed to delete user payments" },
        { status: 400 }
      );
    }

    const { error: profilesError } = await supabaseAdmin
      .from("profiles")
      .delete()
      .eq("id", userId);

    if (profilesError) {
      console.error("Profiles delete error:", profilesError);
      return NextResponse.json(
        { error: "Failed to delete user profile" },
        { status: 400 }
      );
    }

    const { error: trainingsError } = await supabaseAdmin
      .from("trainings")
      .delete()
      .eq("user_id", userId);

    if (trainingsError) {
      console.error("Trainings delete error:", trainingsError);
      return NextResponse.json(
        { error: "Failed to delete user trainings" },
        { status: 400 }
      );
    }

    // =========================
    // DELETE AUTH USER
    // =========================

    const { error: authError } =
      await supabaseAdmin.auth.admin.deleteUser(userId);

    if (authError) {
      console.error("Auth delete error:", authError);
      return NextResponse.json(
        { error: authError.message },
        { status: 400 }
      );
    }

    return NextResponse.json({
      message: "User deleted successfully",
    });

  } catch (err) {
    console.error("Delete account error:", err);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}