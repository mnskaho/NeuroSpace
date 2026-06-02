import type { Metadata } from "next";
import Link from "next/link";
import AppLogo from "@/components/ui/AppLogo";
import AuthForm from "./components/AuthForm";
import QuantumCircuitSVG from "../homepage/components/QuantumCircuitSVG";

export const metadata: Metadata = {
  title: "Sign In — NeuroSpace",
  description: "Access your NeuroSpace quantum ML research platform.",
};

export default function SignUpLoginPage() {
  return (
    <div className="min-h-screen bg-space flex">
      {/* Left Panel — Visual */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden flex-col justify-between p-12"
        style={{ background: "linear-gradient(160deg, #0A0F1E 0%, #0D1428 60%, #111827 100%)" }}>

        {/* Background grid */}
        <div className="absolute inset-0 quantum-grid opacity-50" />

        {/* Glow blobs */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full pointer-events-none"
          style={{ background: "radial-gradient(circle, rgba(124,58,237,0.18) 0%, transparent 70%)" }} />
        <div className="absolute bottom-1/3 right-1/4 w-48 h-48 rounded-full pointer-events-none"
          style={{ background: "radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%)" }} />

        {/* Logo */}
        <Link href="/homepage" className="flex items-center gap-3 relative z-10">
          <AppLogo size={70} />
          <div>
             <span
            className="text-xl font-bold tracking-tight"
            style={{ fontFamily: "var(--ns-font-body)" }}
          >
            Neuro
            <span className="gradient-text-violet font-display italic font-semibold">
              Space
            </span>
          </span>
            <div className="font-mono text-[10px] text-text-muted tracking-widest uppercase">Quantum ML Platform</div>
          </div>
        </Link>

        {/* Circuit visualization */}
        <div className="relative z-10 flex-1 flex flex-col justify-center">
          <div className="glass rounded-2xl p-6 mb-8">
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-2 rounded-full bg-quantum-teal animate-pulse" />
              <span className="font-mono text-xs text-quantum-teal tracking-widest">LIVE CIRCUIT PREVIEW</span>
            </div>
            <div className="h-52">
              <QuantumCircuitSVG />
            </div>
          </div>

          {/* Feature pills */}
          <div className="flex flex-wrap gap-3">
            {[
              "5-qubit QNN",
              "Auto Pipeline",
              "Parallel Training",
              "PDF Export",
              "No Quantum Knowledge Required",
            ].map((f) => (
              <span key={f} className="glass px-3 py-1.5 rounded-full font-mono text-xs text-text-secondary border border-quantum-purple/15">
                {f}
              </span>
            ))}
          </div>
        </div>

      </div>

      {/* Right Panel — Auth Form */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 relative">
        {/* Mobile logo */}
        <Link href="/homepage" className="lg:hidden flex items-center gap-3 mb-8">
          <AppLogo size={48} />
          <span className="font-mono font-bold text-xl text-text-primary">
            Neuro<span className="gradient-text">Space</span>
          </span>
        </Link>

        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="font-mono font-black text-3xl text-text-primary mb-2">
              Welcome Back
            </h1>
            <p className="font-sans text-text-secondary text-sm">
              Access your quantum research platform
            </p>
          </div>

          <AuthForm />
        </div>
      </div>
    </div>
  );
}