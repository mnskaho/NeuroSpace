// "use client";

// import { useState, useEffect } from "react";
// import { createClient } from "@supabase/supabase-js";
// import Icon from "@/components/ui/AppIcon";

// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// export default function ProfilePage() {
//   const [user, setUser] = useState<any>(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchUser = async () => {
//       const { data: { user }, error } = await supabase.auth.getUser();

//       if (error) {
//         console.error("Error fetching user:", error.message);
//       } else {
//         setUser(user);
//       }
//       setLoading(false);
//     };

//     fetchUser();
//   }, []);

//   if (loading) {
//     return (
//       <div className="flex items-center justify-center h-screen bg-space text-text-muted font-mono">
//         Loading profile...
//       </div>
//     );
//   }

//   if (!user) {
//     return (
//       <div className="flex items-center justify-center h-screen bg-space text-red-500 font-mono">
//         No user logged in.
//       </div>
//     );
//   }

//   return (
//     <div className="flex flex-col h-screen bg-space overflow-hidden">
//       {/* Top bar */}
//       <div className="flex items-center justify-between px-6 py-4 border-b border-quantum-purple/10 bg-panel/50 backdrop-blur-sm flex-shrink-0">
//         <div className="flex items-center gap-2 font-mono text-xs text-text-muted">
//           <span>NeuroSpace</span> / <span className="text-quantum-cyan capitalize">Profile</span>
//         </div>
//       </div>

//       {/* Main content */}
//       <div className="flex-1 overflow-y-auto p-6 lg:p-8">
//         <div className="max-w-3xl mx-auto bg-panel rounded-2xl shadow-lg p-8 flex flex-col gap-6">
//           <h1 className="text-2xl font-black font-mono text-text-primary">My Profile</h1>

//           {/* Avatar */}
//           <div className="flex items-center gap-6">
//             <img
//               src={user.user_metadata?.avatar || "/assets/images/no_image.png"}
//               alt="avatar"
//               className="w-24 h-24 rounded-full border-4 border-quantum-cyan shadow-md"
//             />
//             <div className="flex flex-col gap-1">
//               <p className="text-lg font-semibold">{user.user_metadata?.name || "User"}</p>
//               <p className="text-sm text-text-muted">{user.email}</p>
//             </div>
//           </div>

//           {/* Edit profile button */}
//           <button className="flex items-center justify-center gap-2 w-44 py-2 rounded-xl border-2 border-quantum-cyan text-quantum-cyan font-mono text-sm hover:bg-quantum-cyan hover:text-white transition-all duration-300 shadow-md">
//             <Icon name="PencilSquareIcon" size={16} />
//             Edit Profile
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@supabase/supabase-js'
import { ChevronLeft, Edit2, Lock, Eye, EyeOff } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export default function ProfilePage() {

  const router = useRouter()

  const [profile, setProfile] = useState({ name:'', email:'' })
  const [formData, setFormData] = useState({ name:'', email:'' })

  const [loading,setLoading] = useState(true)

  const [passwords,setPasswords] = useState({
    current:'',
    newPassword:'',
    confirm:''
  })

  const [showPassword,setShowPassword] = useState({
    current:false,
    new:false,
    confirm:false
  })

  useEffect(()=>{

    async function fetchProfile(){

      const { data:user,error } = await supabase.auth.getUser()

      if(error || !user?.user){
        console.error(error)
        setLoading(false)
        return
      }

      const fullName = user.user.user_metadata?.full_name || ''

      setProfile({
        name:fullName,
        email:user.user.email || ''
      })

      setFormData({
        name:fullName,
        email:user.user.email || ''
      })

      setLoading(false)
    }

    fetchProfile()

  },[])

  const handleSaveProfile = async()=>{

    const { error } = await supabase.auth.updateUser({
      data:{ full_name:formData.name }
    })

    if(error){
      toast.error(error.message)
      return
    }

    setProfile({...profile,name:formData.name})

    toast.success("Profile updated successfully 🚀")
  }

  const handleChangePassword = async()=>{

    if(passwords.newPassword !== passwords.confirm){
      toast.error("Passwords do not match")
      return
    }

    const { error } = await supabase.auth.updateUser({
      password:passwords.newPassword
    })

    if(error){
      toast.error(error.message)
      return
    }

    toast.success("Password updated successfully 🔐")

    setPasswords({
      current:'',
      newPassword:'',
      confirm:''
    })
  }

  if(loading){
    return(
      <div className="flex min-h-screen items-center justify-center">
        Loading profile...
      </div>
    )
  }

  return(

    <div className="min-h-screen flex items-center justify-center px-4">

      <div className="flex flex-col items-center space-y-10 w-full max-w-lg">

        {/* PROFILE */}

        <div className="quantum-grid glass p-8 rounded-2xl shadow-card w-full space-y-6">

               <div className="sticky top-4 left-4 z-50">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
        >
          Back
        </button>
      </div>


          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Edit2 className="h-5 w-5"/> Edit Profile
          </h2>

          <div className="space-y-2">

            <label className="text-sm">Full Name</label>

            <input
            type="text"
            value={formData.name}
            onChange={(e)=>setFormData({...formData,name:e.target.value})}
            className="input-quantum w-full rounded-lg px-3 py-2"
            />

          </div>

          <div className="space-y-2">

            <label className="text-sm">Email</label>

            <input
            type="email"
            value={formData.email}
            disabled
            className="input-quantum w-full rounded-lg px-3 py-2 bg-gray-800 text-gray-400"
            />

          </div>

          <div className="flex justify-end">

            <button
            onClick={handleSaveProfile}
            className="bg-gradient-to-r from-purple-600 via-cyan-500 to-teal-500 text-white px-4 py-2 rounded-lg text-sm">

              Save Changes

            </button>

          </div>

        </div>


        {/* PASSWORD */}

        <div className="quantum-grid glass p-8 rounded-2xl shadow-card w-full space-y-6">

          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Lock className="h-5 w-5"/> Change Password
          </h2>

          <div className="space-y-4">

            {/* CURRENT */}

            <div className="relative">

              <input
              type={showPassword.current ? "text":"password"}
              placeholder="Current password"
              value={passwords.current}
              onChange={(e)=>setPasswords({...passwords,current:e.target.value})}
              className="input-quantum w-full rounded-lg px-3 py-2"
              />

              <button
              type="button"
              onClick={()=>setShowPassword({...showPassword,current:!showPassword.current})}
              className="absolute right-3 top-2.5">

                {showPassword.current ? <EyeOff size={18}/> : <Eye size={18}/>}

              </button>

            </div>


            {/* NEW */}

            <div className="relative">

              <input
              type={showPassword.new ? "text":"password"}
              placeholder="New password"
              value={passwords.newPassword}
              onChange={(e)=>setPasswords({...passwords,newPassword:e.target.value})}
              className="input-quantum w-full rounded-lg px-3 py-2"
              />

              <button
              type="button"
              onClick={()=>setShowPassword({...showPassword,new:!showPassword.new})}
              className="absolute right-3 top-2.5">

                {showPassword.new ? <EyeOff size={18}/> : <Eye size={18}/>}

              </button>

            </div>


            {/* CONFIRM */}

            <div className="relative">

              <input
              type={showPassword.confirm ? "text":"password"}
              placeholder="Confirm password"
              value={passwords.confirm}
              onChange={(e)=>setPasswords({...passwords,confirm:e.target.value})}
              className="input-quantum w-full rounded-lg px-3 py-2"
              />

              <button
              type="button"
              onClick={()=>setShowPassword({...showPassword,confirm:!showPassword.confirm})}
              className="absolute right-3 top-2.5">

                {showPassword.confirm ? <EyeOff size={18}/> : <Eye size={18}/>}

              </button>

            </div>

            <div className="flex justify-end">

              <button
              onClick={handleChangePassword}
              className="bg-gradient-to-r from-purple-600 via-cyan-500 to-teal-500 text-white px-4 py-2 rounded-lg text-sm">

                Update Password

              </button>

            </div>

          </div>

        </div>

      </div>

    </div>

  )
}