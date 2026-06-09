// "use client";

// import { useState } from "react";

// import Icon from "@/components/ui/AppIcon";

// type Tab = "login" | "signup";

// export default function AuthForm() {
//   const [tab, setTab] = useState<Tab>("login");
//   const [showPassword, setShowPassword] = useState(false);
//   const [loading, setLoading] = useState(false);
//   const [form, setForm] = useState({
//     email: "",
//     password: "",
//     name: "",
//     institution: "",
//     confirmPassword: "",
//   });

//   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
//   };

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);
//     // Mock submit — backend connection point
//     await new Promise((r) => setTimeout(r, 1500));
//     setLoading(false);
//     // Redirect to dashboard after successful auth
//     window.location.href = "/dashboard";
//   };

//   return (
//     <div className="glass rounded-3xl p-8 w-full max-w-md border border-quantum-purple/20">
//       {/* Tabs */}
//       <div className="flex rounded-xl overflow-hidden bg-panel mb-8 p-1 gap-1">
//         {(["login", "signup"] as Tab[]).map((t) => (
//           <button
//             key={t}
//             onClick={() => setTab(t)}
//             className={`flex-1 py-2.5 rounded-lg font-mono text-xs font-semibold tracking-widest uppercase transition-all duration-300 ${
//               tab === t
//                 ? "bg-gradient-quantum text-white shadow-glow-purple"
//                 : "text-text-muted hover:text-text-secondary"
//             }`}
//           >
//             {t === "login" ? "Sign In" : "Sign Up"}
//           </button>
//         ))}
//       </div>

//       {/* OAuth buttons */}
//       <div className="flex flex-col gap-3 mb-6">
//         <button className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border border-quantum-purple/20 bg-panel hover:bg-panel-2 transition-all font-mono text-sm text-text-secondary hover:text-text-primary">
//           <svg className="w-5 h-5" viewBox="0 0 24 24">
//             <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
//             <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
//             <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
//             <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
//           </svg>
//           Continue with Google
//         </button>
//         <button className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border border-quantum-purple/20 bg-panel hover:bg-panel-2 transition-all font-mono text-sm text-text-secondary hover:text-text-primary">
//           <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//             <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
//           </svg>
//           Continue with GitHub
//         </button>
//       </div>

//       {/* Divider */}
//       <div className="flex items-center gap-4 mb-6">
//         <div className="flex-1 h-px bg-quantum-purple/15" />
//         <span className="font-mono text-xs text-text-muted">or</span>
//         <div className="flex-1 h-px bg-quantum-purple/15" />
//       </div>

//       {/* Form */}
//       <form onSubmit={handleSubmit} className="flex flex-col gap-4">
//         {tab === "signup" && (
//           <>
//             <div>
//               <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//                 Full Name
//               </label>
//               <input
//                 name="name"
//                 type="text"
//                 value={form.name}
//                 onChange={handleChange}
//                 placeholder="Dr. Marie Curie"
//                 className="input-quantum w-full px-4 py-3 rounded-xl text-sm"
//                 required
//               />
//             </div>
//             <div>
//               <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//                 Institution
//               </label>
//               <input
//                 name="institution"
//                 type="text"
//                 value={form.institution}
//                 onChange={handleChange}
//                 placeholder="MIT, INRIA, ETH Zürich..."
//                 className="input-quantum w-full px-4 py-3 rounded-xl text-sm"
//               />
//             </div>
//           </>
//         )}

//         <div>
//           <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//             Email
//           </label>
//           <input
//             name="email"
//             type="email"
//             value={form.email}
//             onChange={handleChange}
//             placeholder="researcher@institution.edu"
//             className="input-quantum w-full px-4 py-3 rounded-xl text-sm"
//             required
//           />
//         </div>

//         <div>
//           <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//             Password
//           </label>
//           <div className="relative">
//             <input
//               name="password"
//               type={showPassword ? "text" : "password"}
//               value={form.password}
//               onChange={handleChange}
//               placeholder="••••••••••••"
//               className="input-quantum w-full px-4 py-3 pr-12 rounded-xl text-sm"
//               required
//             />
//             <button
//               type="button"
//               onClick={() => setShowPassword(!showPassword)}
//               className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary transition-colors"
//             >
//               <Icon name={showPassword ? "EyeSlashIcon" : "EyeIcon"} size={18} />
//             </button>
//           </div>
//         </div>

//         {tab === "signup" && (
//           <div>
//             <label className="font-mono text-xs text-text-muted uppercase tracking-wider mb-2 block">
//               Confirm Password
//             </label>
//             <input
//               name="confirmPassword"
//               type="password"
//               value={form.confirmPassword}
//               onChange={handleChange}
//               placeholder="••••••••••••"
//               className="input-quantum w-full px-4 py-3 rounded-xl text-sm"
//               required
//             />
//           </div>
//         )}

//         {tab === "login" && (
//           <div className="flex justify-end">
//             <a href="#" className="font-mono text-xs text-quantum-cyan hover:text-quantum-teal transition-colors">
//               Forgot password?
//             </a>
//           </div>
//         )}

//         <button
//           type="submit"
//           disabled={loading}
//           className="btn-quantum w-full py-4 rounded-xl font-mono text-sm font-semibold mt-2 disabled:opacity-60 disabled:cursor-not-allowed"
//         >
//           <span className="flex items-center justify-center gap-2">
//             {loading ? (
//               <>
//                 <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
//                   <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
//                   <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
//                 </svg>
//                 {tab === "login" ? "Authenticating..." : "Creating account..."}
//               </>
//             ) : (
//               tab === "login" ? "Sign In →" : "Create Research Account →"
//             )}
//           </span>
//         </button>
//       </form>

//       {/* Switch tab */}
//       <p className="text-center font-mono text-xs text-text-muted mt-6">
//         {tab === "login" ? "No account yet? " : "Already have an account? "}
//         <button
//           onClick={() => setTab(tab === "login" ? "signup" : "login")}
//           className="text-quantum-cyan hover:text-quantum-teal transition-colors font-semibold"
//         >
//           {tab === "login" ? "Sign Up" : "Sign In"}
//         </button>
//       </p>

//       <p className="text-center font-mono text-[10px] text-text-muted mt-4">
//         By continuing, you agree to our{" "}
//         <a href="#" className="text-quantum-purple hover:text-quantum-violet">Terms</a> and{" "}
//         <a href="#" className="text-quantum-purple hover:text-quantum-violet">Privacy Policy</a>
//       </p>
//     </div>
//   );
// }

//Correct 

// "use client";

// import { useState, useEffect } from "react";
// import { createClient } from "@supabase/supabase-js";
// import Icon from "@/components/ui/AppIcon";

// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// type Tab = "login" | "signup";

// type ToastType = "success" | "error" | "info";

// interface Toast {
//   id: number;
//   message: string;
//   type: ToastType;
// }

// // ------------------ TOASTS COMPONENT ------------------
// let toastCounter = 0;

// export default function AuthForm() {
//   const [tab, setTab] = useState<Tab>("login");
//   const [showPassword, setShowPassword] = useState(false);
// const [showConfirmPassword, setShowConfirmPassword] = useState(false); // ✅ nouveau state
//   const [loading, setLoading] = useState(false);
//   const [toasts, setToasts] = useState<Toast[]>([]);

//   const [form, setForm] = useState({
//     email: "",
//     password: "",
//     name: "",
//     institution: "",
//     confirmPassword: "",
//   });

//   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
//   };

//   const validatePassword = (password: string) => {
//     const regex =
//       /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=[\]{};':"\\|,.<>/?~-]).{8,}$/;
//     return regex.test(password);
//   };

//   // ---------------- TOAST LOGIC ----------------
//   const addToast = (message: string, type: ToastType = "success") => {
//     const id = toastCounter++;
//     setToasts((prev) => [...prev, { id, message, type }]);
//     setTimeout(() => removeToast(id), 5000);
//   };

//   const removeToast = (id: number) => {
//     setToasts((prev) => prev.filter((t) => t.id !== id));
//   };

//   /* ---------------- LOGIN / SIGNUP ---------------- */
//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);

//     try {
//       if (tab === "login") {
//         const { error } = await supabase.auth.signInWithPassword({
//           email: form.email,
//           password: form.password,
//         });
//         if (error) throw error;
//         window.location.href = "/dashboard";
//       }

//       if (tab === "signup") {
//         if (form.password !== form.confirmPassword) {
//           addToast("⚠️ Passwords do not match", "error");
//           setLoading(false);
//           return;
//         }
//         if (!validatePassword(form.password)) {
//           addToast(
//             "⚠️ Password must be at least 8 characters and include uppercase, lowercase, number, and special character",
//             "error"
//           );
//           setLoading(false);
//           return;
//         }

//         const { data, error } = await supabase.auth.signUp({
//           email: form.email,
//           password: form.password,
//           options: {
//             data: {
//               name: form.name,
//               institution: form.institution,
//             },
//           },
//         });
//         if (error) throw error;

//         if (data.user) {
//           await supabase.from("profiles").upsert({
//             id: data.user.id,
//             name: form.name,
//             email: form.email,
//             institution: form.institution,
//           });
//         }

//         const { error: loginError } = await supabase.auth.signInWithPassword({
//           email: form.email,
//           password: form.password,
//         });
//         if (loginError) throw loginError;

//         addToast("✅ Account created successfully!", "success");

// // ✅ délai avant redirection
// setTimeout(() => {
//   window.location.href = "/dashboard";
// }, 1000);
//       }
//     } catch (err: any) {
//       addToast(`❌ ${err.message || "An unexpected error occurred"}`, "error");
//     }

//     setLoading(false);
//   };

//   /* ---------------- GOOGLE LOGIN ---------------- */
//   const signInWithGoogle = async () => {
//     await supabase.auth.signInWithOAuth({
//       provider: "google",
//       options: { redirectTo: `${window.location.origin}/dashboard` },
//     });
//   };

//   /* ---------------- GITHUB LOGIN ---------------- */
//   const signInWithGithub = async () => {
//     await supabase.auth.signInWithOAuth({
//       provider: "github",
//       options: { redirectTo: `${window.location.origin}/dashboard` },
//     });
//   };

//   /* ---------------- RESET PASSWORD ---------------- */
//   const resetPassword = async () => {
//     if (!form.email) {
//       addToast("⚠️ Enter your email first", "info");
//       return;
//     }

//     const { error } = await supabase.auth.resetPasswordForEmail(form.email, {
//       redirectTo: `${window.location.origin}/reset-password`,
//     });

//     if (error) addToast(`❌ ${error.message}`, "error");
//     else addToast("✅ Password reset email sent. Check your inbox!", "success");
//   };

//   /* ---------------- RENDER ---------------- */
//   return (
//     <div className="relative">
//       {/* ---------------- TOASTS ---------------- */}
//       <div className="fixed top-5 right-5 flex flex-col gap-3 z-50">
//         {toasts.map((t) => (
//           <div
//             key={t.id}
//             className={`flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-mono shadow-lg animate-slide-in ${
//               t.type === "success"
//                 ? "bg-green-500 text-white"
//                 : t.type === "error"
//                 ? "bg-red-500 text-white"
//                 : "bg-blue-500 text-white"
//             }`}
//           >
//             <Icon
//               name={
//                 t.type === "success"
//                   ? "CheckCircleIcon"
//                   : t.type === "error"
//                   ? "XCircleIcon"
//                   : "InformationCircleIcon"
//               }
//               size={18}
//             />
//             <span>{t.message}</span>
//           </div>
//         ))}
//       </div>

//       {/* ---------------- AUTH FORM ---------------- */}
//       <div className="glass rounded-3xl p-8 w-full max-w-md border border-quantum-purple/20">
//         {/* ---------------- TABS ---------------- */}
//         <div className="flex rounded-xl overflow-hidden bg-panel mb-8 p-1 gap-1">
//           {(["login", "signup"] as Tab[]).map((t) => (
//             <button
//               key={t}
//               onClick={() => setTab(t)}
//               className={`flex-1 py-2.5 rounded-lg font-mono text-xs font-semibold tracking-widest uppercase transition-all duration-300 ${
//                 tab === t
//                   ? "bg-gradient-quantum text-white shadow-glow-purple"
//                   : "text-text-muted hover:text-text-secondary"
//               }`}
//             >
//               {t === "login" ? "Sign In" : "Sign Up"}
//             </button>
//           ))}
//         </div>

//         {/* ---------------- OAUTH ---------------- */}
//         <div className="flex flex-col gap-3 mb-6">
//           <button
//             onClick={signInWithGoogle}
//             className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border border-quantum-purple/20 bg-panel hover:bg-panel-2 transition-all font-mono text-sm text-text-secondary hover:text-text-primary"
//           >
//             <svg className="w-5 h-5" viewBox="0 0 24 24">
//               <path
//                 d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
//                 fill="#4285F4"
//               />
//               <path
//                 d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
//                 fill="#34A853"
//               />
//               <path
//                 d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
//                 fill="#FBBC05"
//               />
//               <path
//                 d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
//                 fill="#EA4335"
//               />
//             </svg>
//             Continue with Google
//           </button>

//           <button
//             onClick={signInWithGithub}
//             className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border border-quantum-purple/20 bg-panel hover:bg-panel-2 transition-all font-mono text-sm text-text-secondary hover:text-text-primary"
//           >
//             <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//               <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57
//             0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41
//             -.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795
//             .945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805
//             1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925
//             0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18
//             0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405
//             3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23
//             3.3-1.23.66 1.65.24 2.88.12 3.18.765.84
//             1.23 1.905 1.23 3.225 0 4.605-2.805
//             5.625-5.475 5.925.435.375.81 1.095.81
//             2.22 0 1.605-.015 2.895-.015 3.3
//             0 .315.225.69.825.57A12.02
//             12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
//             </svg>
//             Continue with GitHub
//           </button>
//         </div>

//         {/* ---------------- FORM ---------------- */}
//         <form onSubmit={handleSubmit} className="flex flex-col gap-4">
//           {tab === "signup" && (
//             <>
//               <input
//                 name="name"
//                 type="text"
//                 value={form.name}
//                 onChange={handleChange}
//                 placeholder="Full Name"
//                 className="input-quantum px-4 py-3 rounded-xl text-sm"
//                 required
//               />
//               <input
//                 name="institution"
//                 type="text"
//                 value={form.institution}
//                 onChange={handleChange}
//                 placeholder="Institution"
//                 className="input-quantum px-4 py-3 rounded-xl text-sm"
//               />
//             </>
//           )}

//           <input
//             name="email"
//             type="email"
//             value={form.email}
//             onChange={handleChange}
//             placeholder="Email"
//             className="input-quantum px-4 py-3 rounded-xl text-sm"
//             required
//           />

//           <div className="relative">
//             <input
//               name="password"
//               type={showPassword ? "text" : "password"}
//               value={form.password}
//               onChange={handleChange}
//               placeholder="Password"
//               className="input-quantum w-full px-4 py-3 pr-12 rounded-xl text-sm"
//               required
//             />
//             <button
//               type="button"
//               onClick={() => setShowPassword(!showPassword)}
//               className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted"
//             >
//               <Icon
//                 name={showPassword ? "EyeSlashIcon" : "EyeIcon"}
//                 size={18}
//               />
//             </button>
//           </div>

//           {tab === "signup" && (
//   <div className="relative">
//     <input
//       name="confirmPassword"
//       type={showConfirmPassword ? "text" : "password"} // ✅ utilise le state
//       value={form.confirmPassword}
//       onChange={handleChange}
//       placeholder="Confirm Password"
//       className="input-quantum w-full px-4 py-3 pr-12 rounded-xl text-sm"
//       required
//     />
//     <button
//       type="button"
//       onClick={() => setShowConfirmPassword(!showConfirmPassword)} // ✅ toggle
//       className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted"
//     >
//       <Icon
//         name={showConfirmPassword ? "EyeSlashIcon" : "EyeIcon"} // ✅ icône dynamique
//         size={18}
//       />
//     </button>
//   </div>
// )}

//           {tab === "login" && (
//             <div className="flex justify-end">
//               <button
//                 type="button"
//                 onClick={resetPassword}
//                 className="font-mono text-xs text-quantum-cyan hover:text-quantum-teal transition-colors"
//               >
//                 Forgot password?
//               </button>
//             </div>
//           )}

//          <button
//   type="submit"
//   disabled={loading}
//   className="relative w-full py-4 rounded-xl font-mono text-sm font-semibold
//              text-white bg-gradient-to-r from-purple-600 via-cyan-500 to-teal-400
//              shadow-lg hover:shadow-xl transition-shadow duration-300"
// >
//   <span className="relative z-10">
//     {loading
//       ? "Loading..."
//       : tab === "login"
//       ? "Sign In →"
//       : "Create Account →"}
//   </span>
// </button>
//         </form>

//         {/* ---------------- SWITCH AUTH ---------------- */}
//         <div className="text-center text-xs text-text-muted mt-6">
//           {tab === "login" ? (
//             <>
//               No account yet?{" "}
//               <button
//                 onClick={() => setTab("signup")}
//                 className="text-quantum-cyan hover:text-quantum-teal transition-colors font-semibold"
//               >
//                 Sign Up
//               </button>
//             </>
//           ) : (
//             <>
//               Already have an account?{" "}
//               <button
//                 onClick={() => setTab("login")}
//                 className="text-quantum-cyan hover:text-quantum-teal transition-colors font-semibold"
//               >
                
//                 Sign In
//               </button>
//             </>
//           )}

//           <p className="text-center font-mono text-[10px] text-text-muted mt-4">
//             By continuing, you agree to our{" "}
//             <a
//               href="#"
//               className="text-quantum-purple hover:text-quantum-violet"
//             >
//               Terms
//             </a>{" "}
//             and{" "}
//             <a
//               href="#"
//               className="text-quantum-purple hover:text-quantum-violet"
//             >
//               Privacy Policy
//             </a>
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// }

// Amélioré : 
"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import Icon from "@/components/ui/AppIcon";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type Tab = "login" | "signup";

type ToastType = "success" | "error" | "info";

interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

// ------------------ TOASTS COMPONENT ------------------
let toastCounter = 0;

const getErrorMessage = (error: unknown) => {
  if (error instanceof Error) return error.message;

  if (error && typeof error === "object") {
    const record = error as Record<string, unknown>;
    const message = record.message || record.error_description || record.details || record.hint;
    if (typeof message === "string") return message;
  }

  return "An unexpected error occurred";
};

const getSiteUrl = () => {
  // OAuth should return to the origin the user is actually on, so Vercel never reuses a local env URL.
  if (typeof window !== "undefined") {
    return window.location.origin;
  }

  return process.env.NEXT_PUBLIC_APP_URL || "http://localhost:4028";
};

const getOAuthRedirectUrl = () => `${getSiteUrl()}/oauth-callback`;

export default function AuthForm() {
  const [tab, setTab] = useState<Tab>("login");
  const [showPassword, setShowPassword] = useState(false);
const [showConfirmPassword, setShowConfirmPassword] = useState(false); // ✅ nouveau state
  const [loading, setLoading] = useState(false);
  const [toasts, setToasts] = useState<Toast[]>([]);

  const [form, setForm] = useState({
    email: "",
    password: "",
    name: "",
    institution: "",
    confirmPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const validatePassword = (password: string) => {
    const regex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=[\]{};':"\\|,.<>/?~-]).{8,}$/;
    return regex.test(password);
  };

  // ---------------- TOAST LOGIC ----------------
  const addToast = (message: string, type: ToastType = "success") => {
    const id = toastCounter++;
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => removeToast(id), 5000);
  };

  const removeToast = (id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  /* ---------------- LOGIN / SIGNUP ---------------- */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (tab === "login") {
        const { data, error } = await supabase.auth.signInWithPassword({
          email: form.email,
          password: form.password,
        });
        if (error) throw error;

        if (data.user) {
          const { error: profileError } = await supabase.from("profiles").upsert(
            {
              id: data.user.id,
              email: data.user.email,
              name:
                data.user.user_metadata?.full_name ||
                data.user.user_metadata?.name ||
                data.user.email,
              institution: data.user.user_metadata?.institution || null,
            },
            { onConflict: "id" }
          );
          if (profileError) throw new Error(getErrorMessage(profileError));
        }

        window.location.href = "/dashboard";
      }

      if (tab === "signup") {
        if (form.password !== form.confirmPassword) {
          addToast("⚠️ Passwords do not match", "error");
          setLoading(false);
          return;
        }
        if (!validatePassword(form.password)) {
          addToast(
            "⚠️ Password must be at least 8 characters and include uppercase, lowercase, number, and special character",
            "error"
          );
          setLoading(false);
          return;
        }

        const { data, error } = await supabase.auth.signUp({
          email: form.email,
          password: form.password,
          options: {
            data: {
              name: form.name,
              institution: form.institution,
            },
          },
        });
        if (error) throw error;

        if (data.user) {
          const { error: profileError } = await supabase.from("profiles").upsert(
            {
              id: data.user.id,
              name: form.name,
              email: form.email,
              institution: form.institution,
            },
            { onConflict: "id" }
          );
          if (profileError) throw new Error(getErrorMessage(profileError));
        }

        const { error: loginError } = await supabase.auth.signInWithPassword({
          email: form.email,
          password: form.password,
        });
        if (loginError) throw loginError;

        addToast("✅ Account created successfully!", "success");

// ✅ délai avant redirection
setTimeout(() => {
  window.location.href = "/dashboard";
}, 1000);
      }
    } catch (err: any) {
      addToast(`❌ ${err.message || "An unexpected error occurred"}`, "error");
    }

    setLoading(false);
  };

  /* ---------------- GOOGLE LOGIN ---------------- */
 const signInWithGoogle = async () => {
  setLoading(true);
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: getOAuthRedirectUrl(),
        queryParams: {
          prompt: "select_account", // force Google à afficher le choix du compte
        },
      },
    });
    if (error) throw error;
  } catch (err: any) {
    console.error("Google OAuth error:", err.message);
    addToast(`âŒ ${err.message || "Google sign-in failed"}`, "error");
    setLoading(false);
  }
};

const signInWithGithub = async () => {
  setLoading(true);
  try {
    // On lance l'OAuth GitHub
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "github",
      options: {
        redirectTo: getOAuthRedirectUrl(),
        scopes: "read:user user:email",
      },
    });
    if (error) throw error;

    // --- IMPORTANT ---
    // Supabase gère automatiquement la redirection vers /oauth-callback
    // Tu dois créer cette page pour finaliser le login / signup
  } catch (err: any) {
    console.error("GitHub OAuth error:", err.message);
    addToast(`❌ ${err.message || "GitHub sign-in failed"}`, "error");
    setLoading(false);
  }
};

  /* ---------------- RESET PASSWORD ---------------- */
  const resetPassword = async () => {
    if (!form.email) {
      addToast("⚠️ Enter your email first", "info");
      return;
    }

    const { error } = await supabase.auth.resetPasswordForEmail(form.email, {
      redirectTo: `${window.location.origin}/reset-password`,
    });

    if (error) addToast(`❌ ${error.message}`, "error");
    else addToast("✅ Password reset email sent. Check your inbox!", "success");
  };

  /* ---------------- RENDER ---------------- */
  return (
    <div className="relative">
      {/* ---------------- TOASTS ---------------- */}
      <div className="fixed top-5 right-5 flex flex-col gap-3 z-50">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-mono shadow-lg animate-slide-in ${
              t.type === "success"
                ? "bg-green-500 text-white"
                : t.type === "error"
                ? "bg-red-500 text-white"
                : "bg-blue-500 text-white"
            }`}
          >
            <Icon
              name={
                t.type === "success"
                  ? "CheckCircleIcon"
                  : t.type === "error"
                  ? "XCircleIcon"
                  : "InformationCircleIcon"
              }
              size={18}
            />
            <span>{t.message}</span>
          </div>
        ))}
      </div>

      {/* ---------------- AUTH FORM ---------------- */}
      <div className="glass rounded-3xl p-8 w-full max-w-md border border-quantum-purple/20">
        {/* ---------------- TABS ---------------- */}
        <div className="flex rounded-xl overflow-hidden bg-panel mb-8 p-1 gap-1">
          {(["login", "signup"] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 rounded-lg font-mono text-xs font-semibold tracking-widest uppercase transition-all duration-300 ${
                tab === t
                  ? "bg-gradient-quantum text-white shadow-glow-purple"
                  : "text-text-muted hover:text-text-secondary"
              }`}
            >
              {t === "login" ? "Sign In" : "Sign Up"}
            </button>
          ))}
        </div>

        {/* ---------------- OAUTH ---------------- */}
        <div className="flex flex-col gap-3 mb-6">
          <button
            onClick={signInWithGoogle}
            className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border border-quantum-purple/20 bg-panel hover:bg-panel-2 transition-all font-mono text-sm text-text-secondary hover:text-text-primary"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            Continue with Google
          </button>

        </div>

        {/* ---------------- FORM ---------------- */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {tab === "signup" && (
            <>
              <input
                name="name"
                type="text"
                value={form.name}
                onChange={handleChange}
                placeholder="Full Name"
                className="input-quantum px-4 py-3 rounded-xl text-sm"
                required
              />
              <input
                name="institution"
                type="text"
                value={form.institution}
                onChange={handleChange}
                placeholder="Institution"
                className="input-quantum px-4 py-3 rounded-xl text-sm"
              />
            </>
          )}

          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            placeholder="Email"
            className="input-quantum px-4 py-3 rounded-xl text-sm"
            required
          />

          <div className="relative">
            <input
              name="password"
              type={showPassword ? "text" : "password"}
              value={form.password}
              onChange={handleChange}
              placeholder="Password"
              className="input-quantum w-full px-4 py-3 pr-12 rounded-xl text-sm"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted"
            >
              <Icon
                name={showPassword ? "EyeSlashIcon" : "EyeIcon"}
                size={18}
              />
            </button>
          </div>

          {tab === "signup" && (
  <div className="relative">
    <input
      name="confirmPassword"
      type={showConfirmPassword ? "text" : "password"} // ✅ utilise le state
      value={form.confirmPassword}
      onChange={handleChange}
      placeholder="Confirm Password"
      className="input-quantum w-full px-4 py-3 pr-12 rounded-xl text-sm"
      required
    />
    <button
      type="button"
      onClick={() => setShowConfirmPassword(!showConfirmPassword)} // ✅ toggle
      className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted"
    >
      <Icon
        name={showConfirmPassword ? "EyeSlashIcon" : "EyeIcon"} // ✅ icône dynamique
        size={18}
      />
    </button>
  </div>
)}

          {tab === "login" && (
            <div className="flex justify-end">
              <button
                type="button"
                onClick={resetPassword}
                className="font-mono text-xs text-quantum-cyan hover:text-quantum-teal transition-colors"
              >
                Forgot password?
              </button>
            </div>
          )}

         <button
  type="submit"
  disabled={loading}
  className="relative w-full py-4 rounded-xl font-mono text-sm font-semibold
             text-white bg-gradient-to-r from-purple-600 via-cyan-500 to-teal-400
             shadow-lg hover:shadow-xl transition-shadow duration-300"
>
  <span className="relative z-10">
    {loading
      ? "Loading..."
      : tab === "login"
      ? "Sign In →"
      : "Create Account →"}
  </span>
</button>
        </form>

        {/* ---------------- SWITCH AUTH ---------------- */}
        <div className="text-center text-xs text-text-muted mt-6">
          {tab === "login" ? (
            <>
              No account yet?{" "}
              <button
                onClick={() => setTab("signup")}
                className="text-quantum-cyan hover:text-quantum-teal transition-colors font-semibold"
              >
                Sign Up
              </button>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <button
                onClick={() => setTab("login")}
                className="text-quantum-cyan hover:text-quantum-teal transition-colors font-semibold"
              >
                
                Sign In
              </button>
            </>
          )}

          <p className="text-center font-mono text-[10px] text-text-muted mt-4">
            By continuing, you agree to our{" "}
            <a
              href="#"
              className="text-quantum-purple hover:text-quantum-violet"
            >
              Terms
            </a>{" "}
            and{" "}
            <a
              href="#"
              className="text-quantum-purple hover:text-quantum-violet"
            >
              Privacy Policy
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
