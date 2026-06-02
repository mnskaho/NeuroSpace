// "use client";
// import { useState, useEffect } from "react";
// import { createClient } from "@supabase/supabase-js";

// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// export default function ProfileMenu() {
//   const [user, setUser] = useState<any>(null);
//   const [open, setOpen] = useState(false);

//   useEffect(() => {
//     const fetchUser = async () => {
//       const { data: { user } } = await supabase.auth.getUser();
//       setUser(user);
//     };
//     fetchUser();
//   }, []);

//   const logout = async () => {
//     await supabase.auth.signOut();
//     window.location.href = "/auth"; // Retour page login/signup
//   };

//   if (!user) return null;

//   return (
//     <div className="relative">
//       <button
//         onClick={() => setOpen(!open)}
//         className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold"
//       >
//         {user.user_metadata?.name?.[0]?.toUpperCase() || user.email?.[0].toUpperCase()}
//       </button>

//       {open && (
//         <div className="absolute right-0 mt-2 w-48 bg-panel rounded-xl shadow-lg py-2 flex flex-col gap-2 z-50">
//           {/* User Info */}
//           <div className="px-4 py-2 border-b border-panel/20">
//             <p className="text-sm font-semibold">{user.user_metadata?.name || "User"}</p>
//             <p className="text-xs text-text-muted">{user.email}</p>
//           </div>

//           {/* Menu options */}
//           <button className="px-4 py-2 text-sm hover:bg-panel-2 transition-colors">Profile</button>
//           <button className="px-4 py-2 text-sm hover:bg-panel-2 transition-colors">Settings</button>
//           <button className="px-4 py-2 text-sm hover:bg-panel-2 transition-colors">Help</button>

//           {/* Logout */}
//           <button
//             className="px-4 py-2 text-sm text-red-500 hover:bg-panel-2 transition-colors"
//             onClick={logout}
//           >
//             Logout
//           </button>
//         </div>
//       )}
//     </div>
//   );
// }

"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";
import Icon from "@/components/ui/AppIcon";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function ProfileMenu() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [open, setOpen] = useState(false);

  // ⚡ Récupérer l'utilisateur actuel
  useEffect(() => {
    const fetchUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
    };
    fetchUser();
  }, []);

  // ⚡ Déconnexion
  const logout = async () => {
    await supabase.auth.signOut();
    router.push("/sign-up-login"); // Retour page login/signup
  };

  if (!user) return null; // Ne pas afficher si non connecté

  return (
    <div className="relative">
      {/* Bouton avatar */}
      <button
        onClick={() => setOpen(!open)}
        className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold"
      >
        {user.user_metadata?.name?.[0]?.toUpperCase() || user.email?.[0].toUpperCase()}
      </button>

      {/* Menu déroulant */}
      {open && (
        <div className="absolute right-0 mt-2 w-48 bg-panel rounded-xl shadow-lg py-2 flex flex-col gap-2 z-50">
          
          {/* User Info */}
          <div className="px-4 py-2 border-b border-panel/20">
            <p className="text-sm font-semibold">{user.user_metadata?.name || "User"}</p>
            <p className="text-xs text-text-muted">{user.email}</p>
          </div>

          {/* Menu options */}
          <button
            className="px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
            onClick={() => router.push("/profile")}
          >
            Profile
          </button>

          <button
            className="px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
            onClick={() => router.push("/settings")}
          >
            Settings
          </button>

          <button
            className="px-4 py-2 text-sm hover:bg-panel-2 transition-colors"
            onClick={() => router.push("/help")}
          >
            Help
          </button>

          {/* Logout */}
          <button
            className="px-4 py-2 text-sm text-red-500 hover:bg-panel-2 transition-colors"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}