// "use client";

// import { useRouter } from "next/navigation";
// import { useState } from "react";

// type PaymentMethod = "dahabia" | "paypal" | "stripe" | null;

// export default function PaymentPage() {

//   const router = useRouter();

//   const handleClose = () => {
//     router.back();
//   };

//   const handleSuccess = () => {
//     alert("Paiement réussi !");
//     router.back();
//   };

//   return (
//     <div className="min-h-screen quantum-grid flex items-center justify-center">
//       <PaymentModal onClose={handleClose} onSuccess={handleSuccess} />
//     </div>
//   );
// }

// interface PaymentModalProps {
//   onClose: () => void;
//   onSuccess: () => void;
// }

// function PaymentModal({ onClose, onSuccess }: PaymentModalProps) {

//   const [method, setMethod] = useState<PaymentMethod>(null);
//   const [step, setStep] = useState<"choose" | "form" | "processing" | "done">("choose");

//   const [cardHolder, setCardHolder] = useState("");
//   const [cardNumber, setCardNumber] = useState("");
//   const [expiry, setExpiry] = useState("");
//   const [cvv, setCvv] = useState("");

//   const [formError, setFormError] = useState("");

//   const formatCardNumber = (val: string) =>
//     val.replace(/\D/g, "").slice(0, 16).replace(/(.{4})/g, "$1 ").trim();

//   const formatExpiry = (val: string) => {
//     const digits = val.replace(/\D/g, "").slice(0, 4);
//     if (digits.length >= 3) return `${digits.slice(0, 2)}/${digits.slice(2)}`;
//     return digits;
//   };

//   const simulatePayment = async () => {
//     setStep("processing");
//     await new Promise((r) => setTimeout(r, 2000));
//     setStep("done");
//     await new Promise((r) => setTimeout(r, 800));
//     onSuccess();
//   };

//   const handleDahabiaSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();

//     if (!cardHolder || !cardNumber || !expiry || !cvv) {
//       setFormError("Veuillez remplir tous les champs.");
//       return;
//     }

//     await simulatePayment();
//   };

//   return (
//     <div className="fixed inset-0 flex items-center justify-center bg-black/70 backdrop-blur-md p-4">

//       <div className="relative w-full max-w-md glass rounded-2xl p-7 border border-white/10">

//         <button
//           onClick={onClose}
//           className="absolute top-4 right-4 text-gray-400 hover:text-white"
//         >
//           ✕
//         </button>

//         {/* Processing */}
//         {step === "processing" && (
//           <div className="flex flex-col items-center py-12">

//             <div className="w-14 h-14 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mb-6"></div>

//             <p className="text-white text-lg mb-2">
//               Traitement du paiement...
//             </p>

//             <p className="text-gray-400 text-sm">
//               Merci de patienter
//             </p>

//           </div>
//         )}

//         {/* Success */}
//         {step === "done" && (
//           <div className="flex flex-col items-center py-12">

//             <div className="w-16 h-16 rounded-full bg-green-500/20 border border-green-400 flex items-center justify-center mb-6">
//               ✓
//             </div>

//             <p className="text-green-400 text-xl mb-2">
//               Paiement confirmé !
//             </p>

//             <p className="text-gray-400 text-sm">
//               +1 run ajouté à votre compte
//             </p>

//           </div>
//         )}

//         {/* Choose payment */}
//         {step === "choose" && (
//           <>
//             <div className="mb-6">

//               <h2 className="text-xl font-bold text-white mb-1">
//                 Acheter un run
//               </h2>

//               <p className="text-gray-400 text-sm">
//                 Choisissez votre méthode de paiement
//               </p>

//             </div>

//             {/* Price */}
//             <div className="glass-cyan rounded-xl p-4 mb-6 flex justify-between">

//               <div>
//                 <div className="text-xs text-cyan-400 mb-1">
//                   1 Expérience complète
//                 </div>

//                 <div className="text-2xl font-bold text-white">
//                   4,90 €
//                 </div>
//               </div>

//               <div className="text-3xl">⚗️</div>

//             </div>

//             {/* Stripe */}
//             <button
//               onClick={simulatePayment}
//               className="w-full p-4 mb-3 rounded-xl border border-white/10 glass hover:border-cyan-400/40 flex gap-4"
//             >
//               <div>💠</div>

//               <div className="text-left">
//                 <div className="text-white text-sm">
//                   Carte bancaire
//                 </div>

//                 <div className="text-gray-400 text-xs">
//                   Paiement sécurisé via Stripe
//                 </div>
//               </div>
//             </button>

//             {/* Dahabia */}
//             <button
//               onClick={() => {
//                 setMethod("dahabia");
//                 setStep("form");
//               }}
//               className="w-full p-4 mb-3 rounded-xl border border-white/10 glass hover:border-cyan-400/40 flex gap-4"
//             >
//               <div>💳</div>

//               <div className="text-left">
//                 <div className="text-white text-sm">
//                   Carte Dahabia
//                 </div>

//                 <div className="text-gray-400 text-xs">
//                   Paiement carte CIB
//                 </div>
//               </div>
//             </button>

//             {/* PayPal */}
//             <button
//               onClick={simulatePayment}
//               className="w-full p-4 rounded-xl border border-white/10 glass hover:border-cyan-400/40 flex gap-4"
//             >
//               <div>🅿️</div>

//               <div className="text-left">
//                 <div className="text-white text-sm">
//                   PayPal
//                 </div>

//                 <div className="text-gray-400 text-xs">
//                   Paiement sécurisé PayPal
//                 </div>
//               </div>
//             </button>
//           </>
//         )}

//         {/* Dahabia Form */}
//         {step === "form" && method === "dahabia" && (
//           <form onSubmit={handleDahabiaSubmit} className="space-y-4">

//             <button
//               type="button"
//               onClick={() => setStep("choose")}
//               className="text-gray-400 hover:text-white"
//             >
//               ← Retour
//             </button>

//             {formError && (
//               <div className="text-red-400 text-sm">
//                 {formError}
//               </div>
//             )}

//             <input
//               value={cardHolder}
//               onChange={(e) => setCardHolder(e.target.value)}
//               placeholder="Nom du titulaire"
//               className="input-quantum w-full px-4 py-3 rounded-xl"
//             />

//             <input
//               value={cardNumber}
//               onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
//               placeholder="0000 0000 0000 0000"
//               maxLength={19}
//               className="input-quantum w-full px-4 py-3 rounded-xl"
//             />

//             <div className="grid grid-cols-2 gap-4">

//               <input
//                 value={expiry}
//                 onChange={(e) => setExpiry(formatExpiry(e.target.value))}
//                 placeholder="MM/AA"
//                 maxLength={5}
//                 className="input-quantum px-4 py-3 rounded-xl"
//               />

//               <input
//                 value={cvv}
//                 onChange={(e) =>
//                   setCvv(e.target.value.replace(/\D/g, "").slice(0, 3))
//                 }
//                 placeholder="CVV"
//                 maxLength={3}
//                 className="input-quantum px-4 py-3 rounded-xl"
//               />

//             </div>

//             <button className="btn-quantum w-full py-3 rounded-xl">
//               <span>Payer 4,90 €</span>
//             </button>

//           </form>
//         )}

//       </div>
//     </div>
//   );
// }

// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";

// type PaymentMethod = "credit" | "stripe" | "paypal" | "dahabia";

// export default function PaymentPage() {
//   const router = useRouter();
//   const [method, setMethod] = useState<PaymentMethod>("credit");

//   // Credit Card / Stripe
//   const [cardHolder, setCardHolder] = useState("");
//   const [cardNumber, setCardNumber] = useState("");
//   const [expiry, setExpiry] = useState("");
//   const [cvc, setCvc] = useState("");

//   // Dahabia
//   const [dahabiaHolder, setDahabiaHolder] = useState("");
//   const [dahabiaNumber, setDahabiaNumber] = useState("");
//   const [dahabiaExpiry, setDahabiaExpiry] = useState("");
//   const [dahabiaCVC, setDahabiaCVC] = useState("");

//   const formatCardNumber = (text: string) =>
//     text.replace(/\D/g, "").slice(0, 16).replace(/(.{4})/g, "$1 ").trim();

//   const formatExpiry = (text: string) => {
//     const digits = text.replace(/\D/g, "").slice(0, 4);
//     return digits.length >= 3 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
//   };

//   const handlePayment = () => {
//     if (method === "credit" || method === "stripe") {
//       if (!cardHolder || !cardNumber || !expiry || !cvc) {
//         alert("Please fill all Credit Card / Stripe fields");
//         return;
//       }
//       alert(`Payment simulated via ${method.toUpperCase()} for 30 €`);
//     } else if (method === "dahabia") {
//       if (!dahabiaHolder || !dahabiaNumber || !dahabiaExpiry || !dahabiaCVC) {
//         alert("Please fill all Dahabia fields");
//         return;
//       }
//       alert("Payment simulated via CARTE DAHABIA for 30 €");
//     } else if (method === "paypal") {
//       alert("Redirecting to PayPal for 30 €");
//     }
//   };

//   const payLabel = method === "paypal" ? "CONTINUE TO PAYPAL" : "PAY";

//   return (
//     <div className="min-h-screen quantum-grid flex justify-center items-center px-4 bg-[#0a0a0f]">
//       <div className="glass neon-border rounded-2xl p-10 max-w-lg w-full animate-fadeInUp space-y-6">

//         {/* Back Button with hover glow */}
//         <button
//           onClick={() => router.push("/dashboard")}
//           className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
//         >
//           Back
//         </button>

//         {/* Header */}
//         <div className="text-center mb-6">
//           <div className="w-16 h-16 mx-auto mb-4 rounded-xl flex items-center justify-center glass-cyan">✨</div>
//           <h1 className="text-3xl font-display gradient-text mb-2">Upgrade Plan</h1>
//           <p className="text-text-secondary text-sm">Unlock full access to all features</p>
//         </div>

//         {/* Price Card */}
//         <div className="glass-cyan rounded-xl p-6 text-center mb-6">
//           <div className="text-5xl font-display text-accent-cyan mb-1">30 €</div>
//           <div className="text-text-secondary text-sm mb-3">One-time payment</div>
//           <div className="badge-info px-3 py-1 rounded-full inline-flex items-center gap-2 text-xs">
//             🔒 Secure payment
//           </div>
//         </div>

//         {/* Payment Methods Grid */}
//         <p className="text-xs text-text-secondary mb-3 uppercase font-mono">Mode de Payment</p>
//         <div className="grid grid-cols-2 gap-3 mb-6">

//           {/* Credit Card */}
//           <button
//             onClick={() => setMethod("credit")}
//             className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
//               method === "credit" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"
//             }`}
//           >
//             <div className="w-10 h-10 flex items-center justify-center glass-cyan rounded-lg">💳</div>
//             <div className="flex-1 text-left">
//               <div className="text-sm text-text-primary">Credit Card</div>
//               <div className="text-xs text-text-secondary">Visa / Mastercard</div>
//             </div>
//           </button>

//           {/* Dahabia */}
//           <button
//             onClick={() => setMethod("dahabia")}
//             className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
//               method === "dahabia" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"
//             }`}
//           >
//             <div className="w-10 h-10 flex items-center justify-center glass-cyan rounded-lg">🌍</div>
//             <div className="flex-1 text-left">
//               <div className="text-sm text-text-primary">Carte Dahabia</div>
//               <div className="text-xs text-text-secondary">Algerian payment</div>
//             </div>
//           </button>

//           {/* PayPal */}
//           <button
//             onClick={() => setMethod("paypal")}
//             className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
//               method === "paypal" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"
//             }`}
//           >
//             <div className="w-10 h-10 flex items-center justify-center glass-cyan rounded-lg">🅿️</div>
//             <div className="flex-1 text-left">
//               <div className="text-sm text-text-primary">PayPal</div>
//               <div className="text-xs text-text-secondary">Pay with your account</div>
//             </div>
//           </button>

//         </div>

//         {/* Dynamic Form */}
//         <div className="glass rounded-xl p-6 mb-6 space-y-4">

//           {/* Credit Card / Stripe Form */}
//           {(method === "credit" || method === "stripe") && (
//             <div className="space-y-4">
//               <input
//                 className="input-quantum w-full px-4 py-3 rounded-lg"
//                 placeholder="CARDHOLDER NAME"
//                 value={cardHolder}
//                 onChange={(e) => setCardHolder(e.target.value.toUpperCase())}
//               />
//               <input
//                 className="input-quantum w-full px-4 py-3 rounded-lg"
//                 placeholder="0000 0000 0000 0000"
//                 value={cardNumber}
//                 onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
//               />
//               <div className="grid grid-cols-2 gap-4">
//                 <input
//                   className="input-quantum px-4 py-3 rounded-lg"
//                   placeholder="MM/YY"
//                   value={expiry}
//                   onChange={(e) => setExpiry(formatExpiry(e.target.value))}
//                 />
//                 <input
//                   className="input-quantum px-4 py-3 rounded-lg"
//                   placeholder="CVC"
//                   value={cvc}
//                   onChange={(e) => setCvc(e.target.value.replace(/\D/g, "").slice(0, 3))}
//                 />
//               </div>
//             </div>
//           )}

//           {/* Dahabia Form */}
//           {method === "dahabia" && (
//             <div className="space-y-4">
//               <input
//                 className="input-quantum w-full px-4 py-3 rounded-lg"
//                 placeholder="CARDHOLDER NAME"
//                 value={dahabiaHolder}
//                 onChange={(e) => setDahabiaHolder(e.target.value.toUpperCase())}
//               />
//               <input
//                 className="input-quantum w-full px-4 py-3 rounded-lg"
//                 placeholder="CARD NUMBER"
//                 value={dahabiaNumber}
//                 onChange={(e) => setDahabiaNumber(formatCardNumber(e.target.value))}
//               />
//               <div className="grid grid-cols-2 gap-4">
//                 <input
//                   className="input-quantum px-4 py-3 rounded-lg"
//                   placeholder="MM/YY"
//                   value={dahabiaExpiry}
//                   onChange={(e) => setDahabiaExpiry(formatExpiry(e.target.value))}
//                 />
//                 <input
//                   className="input-quantum px-4 py-3 rounded-lg"
//                   placeholder="CVV"
//                   value={dahabiaCVC}
//                   onChange={(e) =>
//                     setDahabiaCVC(e.target.value.replace(/\D/g, "").slice(0, 3))
//                   }
//                 />
//               </div>
//               <p className="text-xs text-gray-500">🔒 PAIEMENT SÉCURISÉ</p>
//             </div>
//           )}

//           {/* PayPal Form */}
//          {method === "paypal" && (
//   <div className="text-center">
//     <div className="text-4xl mb-4">🅿️</div>
//     <p className="text-text-secondary text-sm mb-4">You will be redirected to PayPal</p>

//     <button
//   className="btn-outline px-6 py-3 rounded-lg"
//   onClick={() => router.push("/payment-success")}
// >
//   Continue to PayPal
// </button>
//   </div>
// )}
//         </div>

//         {/* Pay Button */}
//         {(method !== "paypal") && (
//           <button
//             onClick={handlePayment}
//             className="w-full py-4 rounded-xl text-white font-semibold bg-gradient-to-r from-cyan-400 to-purple-500 hover:opacity-90 transition"
//           >
//             {payLabel}
//           </button>
//         )}

//         <p className="text-center text-xs text-text-muted mt-4">
//           By completing this purchase, you agree to our Terms
//         </p>

//       </div>
//     </div>
//   );
// }


// correct 

// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import { createClient } from "@supabase/supabase-js";

// type PaymentMethod = "credit" | "paypal" | "dahabia";

// const supabase = createClient(
// process.env.NEXT_PUBLIC_SUPABASE_URL!,
// process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// export default function PaymentPage() {

// const router = useRouter();
// const [method,setMethod] = useState<PaymentMethod>("credit");

// const price = 15;

// /* Credit */
// const [cardHolder,setCardHolder] = useState("");
// const [cardNumber,setCardNumber] = useState("");
// const [expiry,setExpiry] = useState("");
// const [cvc,setCvc] = useState("");

// /* Dahabia */
// const [dahabiaHolder, setDahabiaHolder] = useState("");
// const [dahabiaNumber, setDahabiaNumber] = useState("");
// const [dahabiaExpiry, setDahabiaExpiry] = useState("");
// const [dahabiaCVV, setDahabiaCVV] = useState("");

// const formatCardNumber = (text:string)=>
// text.replace(/\D/g,"").slice(0,16).replace(/(.{4})/g,"$1 ").trim();

// const formatExpiry = (text:string)=>{
// const digits = text.replace(/\D/g,"").slice(0,4);
// return digits.length>=3 ? digits.slice(0,2)+"/"+digits.slice(2) : digits;
// };

// /* Save payment in Supabase */

// const savePayment = async(paymentMethod:string)=>{

// const {data:{user}} = await supabase.auth.getUser();

// if(!user) return;

// const invoice = "INV-"+Math.floor(Math.random()*1000000);

// await supabase.from("payments").insert({

// user_id:user.id,
// email:user.email,
// amount:price,
// currency:"EUR",
// payment_method:paymentMethod,
// invoice_number:invoice

// });

// router.push("/payment-success");

// };

// const handlePayment = async()=>{

// if(method==="credit"){

// if(!cardHolder || !cardNumber || !expiry || !cvc){
// alert("Please fill all card fields");
// return;
// }

// await savePayment("Credit Card");

// }

// if(method==="dahabia"){

// if(!dahabiaHolder || !dahabiaNumber || !dahabiaExpiry || !dahabiaCVV){
// alert("Please fill all Dahabia fields");
// return;
// }

// await savePayment("Dahabia");

// }

// };

// return(

// <div className="min-h-screen quantum-grid flex justify-center items-center px-4 bg-[#0a0a0f]">

// <div className="glass neon-border rounded-2xl p-10 max-w-lg w-full animate-fadeInUp space-y-6">

// {/* Back */}

// <button
// onClick={()=>router.push("/dashboard")}
// className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
// >
// Back
// </button>

// {/* Header */}

// <div className="text-center">

// <div className="w-16 h-16 mx-auto mb-4 rounded-xl flex items-center justify-center glass-cyan">
// ✨
// </div>

// <h1 className="text-3xl font-display gradient-text mb-2">
// Upgrade Plan
// </h1>

// <p className="text-text-secondary text-sm">
// Unlock full access to all features
// </p>

// </div>

// {/* Price */}

// <div className="glass-cyan rounded-xl p-6 text-center">

// <div className="text-5xl font-display text-accent-cyan">
// 30 €
// </div>

// <div className="text-text-secondary text-sm mb-3">
// One-time payment
// </div>

// <div className="badge-info px-3 py-1 rounded-full inline-flex items-center gap-2 text-xs">
// 🔒 Secure payment
// </div>

// </div>

// {/* Payment Methods */}

// <p className="text-xs text-text-secondary uppercase font-mono">
// Payment Method
// </p>

// <div className="grid grid-cols-2 gap-3">

// <button
// onClick={()=>setMethod("credit")}
// className={`flex items-center gap-4 p-4 rounded-xl border ${
// method==="credit" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"
// }`}
// >

// <div className="w-10 h-10 flex items-center justify-center glass-cyan rounded-lg">
// 💳
// </div>

// <div className="text-left">
// <div className="text-sm text-text-primary">
// Credit Card
// </div>

// <div className="text-xs text-text-secondary">
// Visa / Mastercard
// </div>

// </div>

// </button>

// <button
// onClick={()=>setMethod("dahabia")}
// className={`flex items-center gap-4 p-4 rounded-xl border ${
// method==="dahabia" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"
// }`}
// >

// <div className="w-10 h-10 flex items-center justify-center glass-cyan rounded-lg">
// 🌍
// </div>

// <div className="text-left">

// <div className="text-sm text-text-primary">
// Carte Dahabia
// </div>

// <div className="text-xs text-text-secondary">
// Algerian payment
// </div>

// </div>

// </button>

// <button
// onClick={()=>setMethod("paypal")}
// className={`flex items-center gap-4 p-4 rounded-xl border ${
// method==="paypal" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"
// }`}
// >

// <div className="w-10 h-10 flex items-center justify-center glass-cyan rounded-lg">
// 🅿️
// </div>

// <div className="text-left">

// <div className="text-sm text-text-primary">
// PayPal
// </div>

// <div className="text-xs text-text-secondary">
// Pay with PayPal
// </div>

// </div>

// </button>

// </div>

// {/* Forms */}

// <div className="glass rounded-xl p-6 space-y-4">

// {method==="credit" &&(

// <>

// <input
// className="input-quantum w-full px-4 py-3 rounded-lg"
// placeholder="CARDHOLDER NAME"
// value={cardHolder}
// onChange={(e)=>setCardHolder(e.target.value.toUpperCase())}
// />

// <input
// className="input-quantum w-full px-4 py-3 rounded-lg"
// placeholder="0000 0000 0000 0000"
// value={cardNumber}
// onChange={(e)=>setCardNumber(formatCardNumber(e.target.value))}
// />

// <div className="grid grid-cols-2 gap-4">

// <input
// className="input-quantum px-4 py-3 rounded-lg"
// placeholder="MM/YY"
// value={expiry}
// onChange={(e)=>setExpiry(formatExpiry(e.target.value))}
// />

// <input
// className="input-quantum px-4 py-3 rounded-lg"
// placeholder="CVC"
// value={cvc}
// onChange={(e)=>setCvc(e.target.value.replace(/\D/g,"").slice(0,3))}
// />

// </div>

// </>

// )}

// {method === "dahabia" && (
//   <>
//     <input
//       className="input-quantum w-full px-4 py-3 rounded-lg"
//       placeholder="CARDHOLDER NAME"
//       value={dahabiaHolder}
//       onChange={(e) => setDahabiaHolder(e.target.value.toUpperCase())}
//     />

//     <input
//       className="input-quantum w-full px-4 py-3 rounded-lg"
//       placeholder="0000 0000 0000 0000"
//       value={dahabiaNumber}
//       onChange={(e) => setDahabiaNumber(formatCardNumber(e.target.value))}
//     />

//     <div className="grid grid-cols-2 gap-4">
//       <input
//         className="input-quantum px-4 py-3 rounded-lg"
//         placeholder="MM/YY"
//         value={dahabiaExpiry}
//         onChange={(e) => setDahabiaExpiry(formatExpiry(e.target.value))}
//       />

//       <input
//         className="input-quantum px-4 py-3 rounded-lg"
//         placeholder="CVV"
//         value={dahabiaCVV}
//         onChange={(e) =>
//           setDahabiaCVV(e.target.value.replace(/\D/g, "").slice(0, 3))
//         }
//       />
//     </div>
//   </>
// )}

// {method==="paypal" &&(

// <div className="text-center">

// <div className="text-4xl mb-4">
// 🅿️
// </div>

// <p className="text-text-secondary text-sm mb-4">
// You will be redirected to PayPal
// </p>

// <button
// className="btn-outline px-6 py-3 rounded-lg"
// onClick={()=>savePayment("PayPal")}
// >
// Continue to PayPal
// </button>

// </div>

// )}

// </div>

// {method!=="paypal" &&(

// <button
// onClick={handlePayment}
// className="w-full py-4 rounded-xl text-white font-semibold bg-gradient-to-r from-cyan-400 to-purple-500 hover:opacity-90 transition"
// >

// Pay

// </button>

// )}

// <p className="text-center text-xs text-text-muted">
// By completing this purchase, you agree to our Terms
// </p>

// </div>

// </div>

// );

// }

// with more plans
// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import { createClient } from "@supabase/supabase-js";
// import { toast } from "sonner";
// import PayPalButton from "./components/PayPalButton";

// type PaymentMethod = "credit" | "paypal" | "dahabia";

// const supabase = createClient(
// process.env.NEXT_PUBLIC_SUPABASE_URL!,
// process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// export default function PaymentPage(){

// const router = useRouter();
// const [method,setMethod] = useState<PaymentMethod>("credit");

// /* PLAN */

// const [selectedPlan,setSelectedPlan] = useState<"Free"|"Pro"|"Enterprise">("Pro");

// const price =
// selectedPlan==="Pro"
// ?15
// :selectedPlan==="Enterprise"
// ?100
// :0;


// /* CREDIT */

// const [cardHolder,setCardHolder] = useState("");
// const [cardNumber,setCardNumber] = useState("");
// const [expiry,setExpiry] = useState("");
// const [cvc,setCvc] = useState("");

// /* DAHABIA */

// const [dahabiaHolder,setDahabiaHolder] = useState("");
// const [dahabiaNumber,setDahabiaNumber] = useState("");
// const [dahabiaExpiry,setDahabiaExpiry] = useState("");
// const [dahabiaCVV,setDahabiaCVV] = useState("");

// /* FORMAT */

// const formatCardNumber = (text:string)=>
// text.replace(/\D/g,"").slice(0,16).replace(/(.{4})/g,"$1 ").trim();

// const formatExpiry = (text:string)=>{
// const digits=text.replace(/\D/g,"").slice(0,4);
// return digits.length>=3
// ?digits.slice(0,2)+"/"+digits.slice(2)
// :digits;
// };

// /* SAVE PAYMENT */

// const savePayment = async(paymentMethod:string)=>{

// const {data:{user}} = await supabase.auth.getUser();

// if(!user){
// toast.error("User not authenticated");
// return;
// }

// const invoice="INV-"+Math.floor(Math.random()*1000000);

// const {error} = await supabase.from("payments").insert({

// user_id:user.id,
// email:user.email,
// amount:price,
// currency:"EUR",
// payment_method:paymentMethod,
// invoice_number:invoice,
// plan:selectedPlan

// });

// if(error){
// toast.error("Payment failed");
// return;
// }

// router.push("/payment-success");

// };


// /* HANDLE PAYMENT */

// const handlePayment = async()=>{

// if(selectedPlan==="Free"){
// router.push("/dashboard");
// return;
// }

// /* CREDIT */

// if(method==="credit"){

// if(!cardHolder || !cardNumber || !expiry || !cvc){
// toast.error("Please fill all credit card fields 💳");
// return;
// }

// const loading = toast.loading("Processing payment...");

// await savePayment("Credit Card");

// toast.dismiss(loading);
// toast.success("Payment completed successfully");

// }


// /* DAHABIA */

// if(method==="dahabia"){

// if(!dahabiaHolder || !dahabiaNumber || !dahabiaExpiry || !dahabiaCVV){
// toast.error("Please fill all Dahabia fields 💳");
// return;
// }

// const loading = toast.loading("Processing Dahabia payment...");

// await savePayment("Dahabia");

// toast.dismiss(loading);
// toast.success("Dahabia payment completed");

// }

// };


// /* UI */

// return(

// <div className="min-h-screen quantum-grid flex justify-center items-center px-4 bg-[#0a0a0f]">

// <div className="glass neon-border rounded-2xl p-10 max-w-lg w-full animate-fadeInUp space-y-6">

// {/* BACK */}

// <button
// onClick={()=>router.push("/dashboard")}
// className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105"
// >
// Back
// </button>


// {/* HEADER */}

// <div className="text-center">

// <div className="w-16 h-16 mx-auto mb-4 rounded-xl flex items-center justify-center glass-cyan">
// ✨
// </div>

// <h1 className="text-3xl font-display gradient-text mb-2">
// Upgrade Plan
// </h1>

// <p className="text-text-secondary text-sm">
// Unlock full access to all features
// </p>

// </div>


// {/* PLANS */}

// <div className="grid grid-cols-3 gap-3">

// {[
// {plan:"Free",price:"0€",train:"1"},
// {plan:"Pro",price:"30€ / month",train:"25"},
// {plan:"Enterprise",price:"100€ / month",train:"Unlimited"}
// ].map((p)=>(

// <button
// key={p.plan}
// onClick={()=>setSelectedPlan(p.plan as any)}
// className={`rounded-xl border p-4 text-center transition ${
// selectedPlan===p.plan
// ?"border-accent-cyan bg-accent-cyan/10"
// :"border-border glass hover:border-accent-cyan/40"
// }`}
// >

// <div className="text-sm font-semibold text-text-primary">
// {p.plan}
// </div>

// <div className="text-xs text-text-secondary mt-1">
// {p.price}
// </div>

// <div className="text-xs mt-2 text-accent-cyan">
// {p.train} Trainings
// </div>

// </button>

// ))}

// </div>


// {/* PRICE */}

// <div className="glass-cyan rounded-xl p-6 text-center">

// <div className="text-5xl font-display text-accent-cyan">
// {price} €
// </div>

// <div className="text-text-secondary text-sm mb-3">
// {selectedPlan==="Free"?"Free plan":"Monthly subscription"}
// </div>

// <div className="badge-info px-3 py-1 rounded-full inline-flex items-center gap-2 text-xs">
// 🔒 Secure payment
// </div>

// </div>


// {/* PAYMENT METHODS */}

// <p className="text-xs text-text-secondary uppercase font-mono">
// Payment Method
// </p>

// <div className="grid grid-cols-3 gap-3">

// <button
// onClick={()=>setMethod("credit")}
// className={`p-4 rounded-xl border ${
// method==="credit"
// ?"border-accent-cyan bg-accent-cyan/10"
// :"border-border glass"
// }`}
// >
// 💳 Credit Card
// </button>

// <button
// onClick={()=>setMethod("dahabia")}
// className={`p-4 rounded-xl border ${
// method==="dahabia"
// ?"border-accent-cyan bg-accent-cyan/10"
// :"border-border glass"
// }`}
// >
// 🌍 Dahabia
// </button>

// <button
// onClick={()=>setMethod("paypal")}
// className={`p-4 rounded-xl border ${
// method==="paypal"
// ?"border-accent-cyan bg-accent-cyan/10"
// :"border-border glass"
// }`}
// >
// 🅿️ PayPal
// </button>

// </div>


// {/* FORM */}

// <div className="glass rounded-xl p-6 space-y-4">

// {method==="credit"&&(

// <>

// <input
// className="input-quantum w-full px-4 py-3 rounded-lg"
// placeholder="CARDHOLDER NAME"
// value={cardHolder}
// onChange={(e)=>setCardHolder(e.target.value.toUpperCase())}
// />

// <input
// className="input-quantum w-full px-4 py-3 rounded-lg"
// placeholder="0000 0000 0000 0000"
// value={cardNumber}
// onChange={(e)=>setCardNumber(formatCardNumber(e.target.value))}
// />

// <div className="grid grid-cols-2 gap-4">

// <input
// className="input-quantum px-4 py-3 rounded-lg"
// placeholder="MM/YY"
// value={expiry}
// onChange={(e)=>setExpiry(formatExpiry(e.target.value))}
// />

// <input
// className="input-quantum px-4 py-3 rounded-lg"
// placeholder="CVC"
// value={cvc}
// onChange={(e)=>setCvc(e.target.value.replace(/\D/g,"").slice(0,3))}
// />

// </div>

// </>

// )}


// {method==="dahabia"&&(

// <>

// <input
// className="input-quantum w-full px-4 py-3 rounded-lg"
// placeholder="CARDHOLDER NAME"
// value={dahabiaHolder}
// onChange={(e)=>setDahabiaHolder(e.target.value.toUpperCase())}
// />

// <input
// className="input-quantum w-full px-4 py-3 rounded-lg"
// placeholder="0000 0000 0000 0000"
// value={dahabiaNumber}
// onChange={(e)=>setDahabiaNumber(formatCardNumber(e.target.value))}
// />

// <div className="grid grid-cols-2 gap-4">

// <input
// className="input-quantum px-4 py-3 rounded-lg"
// placeholder="MM/YY"
// value={dahabiaExpiry}
// onChange={(e)=>setDahabiaExpiry(formatExpiry(e.target.value))}
// />

// <input
// className="input-quantum px-4 py-3 rounded-lg"
// placeholder="CVV"
// value={dahabiaCVV}
// onChange={(e)=>setDahabiaCVV(e.target.value.replace(/\D/g,"").slice(0,3))}
// />

// </div>

// </>

// )}


// {method==="paypal"&&(

// <div className="text-center">

// <p className="text-sm text-text-secondary mb-4">
// You will be redirected to PayPal
// </p>

// <button
// onClick={()=>savePayment("PayPal")}
// className="btn-outline px-6 py-3 rounded-lg"
// >
// Continue to PayPal
// </button>

// </div>

// )}

// </div>


// {method!=="paypal"&&(

// <button
// onClick={handlePayment}
// className="w-full py-4 rounded-xl text-white font-semibold bg-gradient-to-r from-cyan-400 to-purple-500 hover:opacity-90 transition"
// >
// {selectedPlan==="Free"?"Activate Free Plan":"Pay"}
// </button>

// )}

// <p className="text-center text-xs text-text-muted">
// By completing this purchase you agree to our Terms
// </p>

// </div>

// </div>

// );

// }

// with more plans
// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import { createClient } from "@supabase/supabase-js";
// import { toast } from "sonner";
// import PayPalButton from "./components/PayPalButton";
// import emailjs from "@emailjs/browser";

// type PaymentMethod = "credit" | "paypal" | "dahabia";

// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// export default function PaymentPage() {
//   const router = useRouter();
//   const [method, setMethod] = useState<PaymentMethod>("credit");
//   const [selectedPlan, setSelectedPlan] = useState<"Free" | "Pro" | "Enterprise">("Pro");

//   const price = selectedPlan === "Pro" ? 30 : selectedPlan === "Enterprise" ? 100 : 0;

//   /* Credit */
//   const [cardHolder, setCardHolder] = useState("");
//   const [cardNumber, setCardNumber] = useState("");
//   const [expiry, setExpiry] = useState("");
//   const [cvc, setCvc] = useState("");

//   /* Dahabia */
//   const [dahabiaHolder, setDahabiaHolder] = useState("");
//   const [dahabiaNumber, setDahabiaNumber] = useState("");
//   const [dahabiaExpiry, setDahabiaExpiry] = useState("");
//   const [dahabiaCVV, setDahabiaCVV] = useState("");

//   /* Format helpers */
//   const formatCardNumber = (text: string) =>
//     text.replace(/\D/g, "").slice(0, 16).replace(/(.{4})/g, "$1 ").trim();

//   const formatExpiry = (text: string) => {
//     const digits = text.replace(/\D/g, "").slice(0, 4);
//     return digits.length >= 3 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
//   };

//   /* Send invoice via EmailJS */
//   const sendInvoiceEmail = async (user: any, invoice: string, amount: number, plan: string) => {
//     try {
//       await emailjs.send(
//         process.env.NEXT_PUBLIC_EMAILJS_SERVICE_ID!,
//         process.env.NEXT_PUBLIC_EMAILJS_TEMPLATE_ID!,
//         {
//           user_name: user.user_metadata.full_name || user.email,
//           user_email: user.email,
//           plan,
//           amount,
//           invoice_number: invoice,
//           date: new Date().toLocaleDateString(),
//         },
//         process.env.NEXT_PUBLIC_EMAILJS_PUBLIC_KEY!
//       );
//       console.log("Invoice email sent via EmailJS ✅");
//     } catch (err) {
//       console.error("Failed to send invoice email via EmailJS:", err);
//     }
//   };

//   /* Save payment to Supabase + send invoice */
//   const savePayment = async (paymentMethod: string) => {
//     const { data: { user } } = await supabase.auth.getUser();
//     if (!user) {
//       toast.error("User not authenticated");
//       return;
//     }

//     const invoice = "INV-" + Math.floor(Math.random() * 1000000);

//     const { error } = await supabase.from("payments").insert({
//       user_id: user.id,
//       email: user.email,
//       amount: price,
//       currency: "EUR",
//       payment_method: paymentMethod,
//       invoice_number: invoice,
//       plan: selectedPlan,
//     });

//     if (error) {
//       toast.error("Payment failed ❌");
//       return;
//     }

//     // Send invoice via EmailJS
//     await sendInvoiceEmail(user, invoice, price, selectedPlan);

//     toast.success("Payment completed successfully ✅");
//     router.push("/payment-success");
//   };

//   /* Handle payment click for Credit / Dahabia */
//   const handlePayment = async () => {
//     if (selectedPlan === "Free") {
//       router.push("/dashboard");
//       return;
//     }

//     if (method === "credit") {
//       if (!cardHolder || !cardNumber || !expiry || !cvc) {
//         toast.error("Please fill all credit card fields 💳");
//         return;
//       }

//       const loading = toast.loading("Processing credit card payment...");
//       await savePayment("Credit Card");
//       toast.dismiss(loading);
//     }

//     if (method === "dahabia") {
//       if (!dahabiaHolder || !dahabiaNumber || !dahabiaExpiry || !dahabiaCVV) {
//         toast.error("Please fill all Dahabia fields 💳");
//         return;
//       }

//       const loading = toast.loading("Processing Dahabia payment...");
//       await savePayment("Dahabia");
//       toast.dismiss(loading);
//     }
//   };

//   return (
//     <div className="min-h-screen quantum-grid flex justify-center items-center px-4 bg-[#0a0a0f]">
//       <div className="glass neon-border rounded-2xl p-10 max-w-lg w-full animate-fadeInUp space-y-6">
//         {/* Back */}
//         <button
//           onClick={() => router.push("/dashboard")}
//           className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105"
//         >
//           Back
//         </button>

//         {/* Header */}
//         <div className="text-center">
//           <div className="w-16 h-16 mx-auto mb-4 rounded-xl flex items-center justify-center glass-cyan">✨</div>
//           <h1 className="text-3xl font-display gradient-text mb-2">Upgrade Plan</h1>
//           <p className="text-text-secondary text-sm">Unlock full access to all features</p>
//         </div>

//         {/* Plans */}
//         <div className="grid grid-cols-3 gap-3">
//           {[
//             { plan: "Free", price: "0€", train: "1" },
//             { plan: "Pro", price: "30€ / month", train: "25" },
//             { plan: "Enterprise", price: "100€ / month", train: "Unlimited" },
//           ].map((p) => (
//             <button
//               key={p.plan}
//               onClick={() => setSelectedPlan(p.plan as any)}
//               className={`rounded-xl border p-4 text-center transition ${
//                 selectedPlan === p.plan ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass hover:border-accent-cyan/40"
//               }`}
//             >
//               <div className="text-sm font-semibold text-text-primary">{p.plan}</div>
//               <div className="text-xs text-text-secondary mt-1">{p.price}</div>
//               <div className="text-xs mt-2 text-accent-cyan">{p.train} Trainings</div>
//             </button>
//           ))}
//         </div>

//         {/* Price */}
//         <div className="glass-cyan rounded-xl p-6 text-center">
//           <div className="text-5xl font-display text-accent-cyan">{price} €</div>
//           <div className="text-text-secondary text-sm mb-3">{selectedPlan === "Free" ? "Free plan" : "Monthly subscription"}</div>
//           <div className="badge-info px-3 py-1 rounded-full inline-flex items-center gap-2 text-xs">🔒 Secure payment</div>
//         </div>

//         {/* Payment Methods */}
//         <p className="text-xs text-text-secondary uppercase font-mono">Payment Method</p>
//         <div className="grid grid-cols-3 gap-3">
//           <button onClick={() => setMethod("credit")} className={`p-4 rounded-xl border ${method === "credit" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"}`}>💳 Credit Card</button>
//           <button onClick={() => setMethod("dahabia")} className={`p-4 rounded-xl border ${method === "dahabia" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"}`}>🌍 Dahabia</button>
//           <button onClick={() => setMethod("paypal")} className={`p-4 rounded-xl border ${method === "paypal" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"}`}>🅿️ PayPal</button>
//         </div>

//         {/* Form / PayPal */}
//         <div className="glass rounded-xl p-6 space-y-4">
//           {method === "credit" && (
//             <>
//               <input className="input-quantum w-full px-4 py-3 rounded-lg" placeholder="CARDHOLDER NAME" value={cardHolder} onChange={(e) => setCardHolder(e.target.value.toUpperCase())} />
//               <input className="input-quantum w-full px-4 py-3 rounded-lg" placeholder="0000 0000 0000 0000" value={cardNumber} onChange={(e) => setCardNumber(formatCardNumber(e.target.value))} />
//               <div className="grid grid-cols-2 gap-4">
//                 <input className="input-quantum px-4 py-3 rounded-lg" placeholder="MM/YY" value={expiry} onChange={(e) => setExpiry(formatExpiry(e.target.value))} />
//                 <input className="input-quantum px-4 py-3 rounded-lg" placeholder="CVC" value={cvc} onChange={(e) => setCvc(e.target.value.replace(/\D/g, "").slice(0, 3))} />
//               </div>
//             </>
//           )}

//           {method === "dahabia" && (
//             <>
//               <input className="input-quantum w-full px-4 py-3 rounded-lg" placeholder="CARDHOLDER NAME" value={dahabiaHolder} onChange={(e) => setDahabiaHolder(e.target.value.toUpperCase())} />
//               <input className="input-quantum w-full px-4 py-3 rounded-lg" placeholder="0000 0000 0000 0000" value={dahabiaNumber} onChange={(e) => setDahabiaNumber(formatCardNumber(e.target.value))} />
//               <div className="grid grid-cols-2 gap-4">
//                 <input className="input-quantum px-4 py-3 rounded-lg" placeholder="MM/YY" value={dahabiaExpiry} onChange={(e) => setDahabiaExpiry(formatExpiry(e.target.value))} />
//                 <input className="input-quantum px-4 py-3 rounded-lg" placeholder="CVV" value={dahabiaCVV} onChange={(e) => setDahabiaCVV(e.target.value.replace(/\D/g, "").slice(0, 3))} />
//               </div>
//             </>
//           )}

//           {/* {method === "paypal" && (
//             <div className="text-center">
//               <p className="text-sm text-text-secondary mb-4">Pay securely with PayPal</p>
//               <PayPalButton
//                 amount={price}
//                 onSuccess={async () => {
//                   await savePayment("PayPal");
//                 }}
//               />
//             </div>
//           )} */}

//           {method === "paypal" && (
//   <div className="text-center">
//     <p className="text-sm text-text-secondary mb-4">
//       Pay securely with PayPal
//     </p>

//     <PayPalButton
//       amount={price}
//       plan={selectedPlan} // 🔥 AJOUT ICI
//       onSuccess={async () => await savePayment("PayPal")}
//     />
//   </div>
// )}
//         </div>

//         {/* Button pour Credit / Dahabia */}
//         {method !== "paypal" && (
//           <button onClick={handlePayment} className="w-full py-4 rounded-xl text-white font-semibold bg-gradient-to-r from-cyan-400 to-purple-500 hover:opacity-90 transition">
//             {selectedPlan === "Free" ? "Activate Free Plan" : "Pay"}
//           </button>
//         )}

//         <p className="text-center text-xs text-text-muted">By completing this purchase you agree to our Terms</p>
//       </div>
//     </div>
//   );
// }

// code complet with email invoice and more plans
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@supabase/supabase-js";
import { toast } from "sonner";
import PayPalButton from "./components/PayPalButton";
import emailjs from "@emailjs/browser";

type PaymentMethod = "credit" | "paypal" | "dahabia";
type PlanType = "Free" | "Pro" | "Pro+";

const plans: Array<{
  plan: PlanType;
  price: number;
  priceLabel: string;
  trainingLabel: string;
}> = [
  { plan: "Free", price: 0, priceLabel: "0€", trainingLabel: "1 Trainings" },
  { plan: "Pro", price: 150, priceLabel: "150€ / month", trainingLabel: "5 Trainings" },
  { plan: "Pro+", price: 500, priceLabel: "500€ / month", trainingLabel: "25 Trainings" },
];

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function PaymentPage() {
  const router = useRouter();

  const [method, setMethod] = useState<PaymentMethod>("credit");
  const [selectedPlan, setSelectedPlan] = useState<PlanType>("Pro");

  const price = plans.find((item) => item.plan === selectedPlan)?.price ?? 0;

  // Credit card
  const [cardHolder, setCardHolder] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvc, setCvc] = useState("");

  // Dahabia
  const [dahabiaHolder, setDahabiaHolder] = useState("");
  const [dahabiaNumber, setDahabiaNumber] = useState("");
  const [dahabiaExpiry, setDahabiaExpiry] = useState("");
  const [dahabiaCVV, setDahabiaCVV] = useState("");

  // --- Helpers ---
  const formatCardNumber = (text: string) =>
    text.replace(/\D/g, "").slice(0, 16).replace(/(.{4})/g, "$1 ").trim();

  const formatExpiry = (text: string) => {
    const digits = text.replace(/\D/g, "").slice(0, 4);
    return digits.length >= 3 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
  };

  // --- Send Invoice Email to Admin only ---
  const sendInvoiceEmailToAdmin = async (user: any, invoice: string) => {
    try {
      await emailjs.send(
        process.env.NEXT_PUBLIC_EMAILJS_SERVICE_ID!,
        process.env.NEXT_PUBLIC_EMAILJS_ADMIN_TEMPLATE_ID!, // template_z056pgn
        {
          user_name: user.user_metadata.full_name || user.email,
          user_email: user.email,
          plan: selectedPlan,
          amount: price,
          invoice_number: invoice,
          date: new Date().toLocaleDateString(),
          admin_email: process.env.NEXT_PUBLIC_ADMIN_EMAIL,
        },
        process.env.NEXT_PUBLIC_EMAILJS_PUBLIC_KEY!
      );
      console.log("Invoice email sent to admin ✅");
    } catch (err) {
      console.error("Failed to send invoice email to admin:", err);
    }
  };

  // --- Save Payment + Send Email to Admin + Redirect ---
  const savePayment = async (paymentMethod: string) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error("User not authenticated");

      const invoice = "INV-" + Math.floor(Math.random() * 1000000);

      const { error } = await supabase.from("payments").insert({
        user_id: user.id,
        email: user.email,
        amount: price,
        currency: "EUR",
        payment_method: paymentMethod,
        invoice_number: invoice,
        plan: selectedPlan,
      });

      if (error) throw error;

      // ✅ Send only to admin
      await sendInvoiceEmailToAdmin(user, invoice);

      toast.success("Payment completed successfully ✅");

      // Redirect to success page
      router.push("/payment-success");
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Payment failed ❌");
    }
  };

  // --- Handle Payment Click ---
  const handlePayment = async () => {
    if (selectedPlan === "Free") {
      router.push("/dashboard");
      return;
    }

    if (method === "credit") {
      if (!cardHolder || !cardNumber || !expiry || !cvc) {
        toast.error("Please fill all credit card fields 💳");
        return;
      }
      const loading = toast.loading("Processing credit card payment...");
      await savePayment("Credit Card");
      toast.dismiss(loading);
    }

    if (method === "dahabia") {
      if (!dahabiaHolder || !dahabiaNumber || !dahabiaExpiry || !dahabiaCVV) {
        toast.error("Please fill all Dahabia fields 💳");
        return;
      }
      const loading = toast.loading("Processing Dahabia payment...");
      await savePayment("Dahabia");
      toast.dismiss(loading);
    }
  };

  // --- UI ---
  return (
    <div className="min-h-screen quantum-grid flex justify-center items-center px-4 bg-[#0a0a0f]">
      <div className="glass neon-border rounded-2xl p-10 max-w-lg w-full animate-fadeInUp space-y-6">

        {/* Back Button */}
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105"
        >
          Back
        </button>

        {/* Header */}
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-xl flex items-center justify-center glass-cyan">✨</div>
          <h1 className="text-3xl font-display gradient-text mb-2">Upgrade Plan</h1>
          <p className="text-text-secondary text-sm">Unlock full access to all features</p>
        </div>

        {/* Plans */}
        <div className="grid grid-cols-3 gap-3">
          {plans.map((p) => (
            <button
              key={p.plan}
              onClick={() => setSelectedPlan(p.plan)}
              className={`rounded-xl border p-4 text-center transition ${
                selectedPlan === p.plan ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass hover:border-accent-cyan/40"
              }`}
            >
              <div className="text-sm font-semibold text-text-primary">{p.plan}</div>
              <div className="text-xs text-text-secondary mt-1">{p.priceLabel}</div>
              <div className="text-xs mt-2 text-accent-cyan">{p.trainingLabel}</div>
            </button>
          ))}
        </div>

        {/* Price */}
        <div className="glass-cyan rounded-xl p-6 text-center">
          <div className="text-5xl font-display text-accent-cyan">{price} €</div>
          <div className="text-text-secondary text-sm mb-3">
            {selectedPlan === "Free" ? "Free plan" : "Monthly subscription"}
          </div>
          <div className="badge-info px-3 py-1 rounded-full inline-flex items-center gap-2 text-xs">🔒 Secure payment</div>
        </div>

        {/* Payment Methods */}
        <p className="text-xs text-text-secondary uppercase font-mono">Payment Method</p>
        <div className="grid grid-cols-3 gap-3">
          <button onClick={() => setMethod("credit")} className={`p-4 rounded-xl border ${method === "credit" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"}`}>💳 Credit Card</button>
          <button onClick={() => setMethod("dahabia")} className={`p-4 rounded-xl border ${method === "dahabia" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"}`}>🌍 Dahabia</button>
          <button onClick={() => setMethod("paypal")} className={`p-4 rounded-xl border ${method === "paypal" ? "border-accent-cyan bg-accent-cyan/10" : "border-border glass"}`}>🅿️ PayPal</button>
        </div>

        {/* Payment Form */}
        <div className="glass rounded-xl p-6 space-y-4">
          {method === "credit" && (
            <>
              <input placeholder="CARDHOLDER NAME" value={cardHolder} onChange={e => setCardHolder(e.target.value.toUpperCase())} className="input-quantum w-full px-4 py-3 rounded-lg" />
              <input placeholder="0000 0000 0000 0000" value={cardNumber} onChange={e => setCardNumber(formatCardNumber(e.target.value))} className="input-quantum w-full px-4 py-3 rounded-lg" />
              <div className="grid grid-cols-2 gap-4">
                <input placeholder="MM/YY" value={expiry} onChange={e => setExpiry(formatExpiry(e.target.value))} className="input-quantum px-4 py-3 rounded-lg" />
                <input placeholder="CVC" value={cvc} onChange={e => setCvc(e.target.value.replace(/\D/g, "").slice(0,3))} className="input-quantum px-4 py-3 rounded-lg" />
              </div>
            </>
          )}

          {method === "dahabia" && (
            <>
              <input placeholder="CARDHOLDER NAME" value={dahabiaHolder} onChange={e => setDahabiaHolder(e.target.value.toUpperCase())} className="input-quantum w-full px-4 py-3 rounded-lg" />
              <input placeholder="0000 0000 0000 0000" value={dahabiaNumber} onChange={e => setDahabiaNumber(formatCardNumber(e.target.value))} className="input-quantum w-full px-4 py-3 rounded-lg" />
              <div className="grid grid-cols-2 gap-4">
                <input placeholder="MM/YY" value={dahabiaExpiry} onChange={e => setDahabiaExpiry(formatExpiry(e.target.value))} className="input-quantum px-4 py-3 rounded-lg" />
                <input placeholder="CVV" value={dahabiaCVV} onChange={e => setDahabiaCVV(e.target.value.replace(/\D/g, "").slice(0,3))} className="input-quantum px-4 py-3 rounded-lg" />
              </div>
            </>
          )}

          {method === "paypal" && (
            <div className="text-center">
              <p className="text-sm text-text-secondary mb-4">Pay securely with PayPal</p>
              <PayPalButton
                amount={price}
                plan={selectedPlan}
                onSuccess={async () => await savePayment("PayPal")}
              />
            </div>
          )}
        </div>

        {/* Credit / Dahabia Button */}
        {method !== "paypal" && (
          <button onClick={handlePayment} className="w-full py-4 rounded-xl text-white font-semibold bg-gradient-to-r from-cyan-400 to-purple-500 hover:opacity-90 transition">
            {selectedPlan === "Free" ? "Activate Free Plan" : "Pay"}
          </button>
        )}

        <p className="text-center text-xs text-text-muted">By completing this purchase you agree to our Terms</p>
      </div>
    </div>
  );
}
