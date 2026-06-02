"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import QuantumCircuitSVG from "./QuantumCircuitSVG";

const floatingCards = [
  {
    label: "QNN Accuracy",
    value: "94.7%",
    delta: "+3.2% vs Classical",
    color: "cyan",
    icon: "⚡",
    style: "top-[15%] right-[2%] animate-float",
  },
  {
    label: "Circuit Depth",
    value: "12 layers",
    delta: "5 qubits",
    color: "purple",
    icon: "◈",
    style: "top-[55%] right-[3%] animate-float-delayed",
  },
  {
    label: "F1-Score",
    value: "0.943",
    delta: "Precision: 0.951",
    color: "teal",
    icon: "◎",
    style: "bottom-[12%] right-[8%] animate-float-slow",
  },
];

export default function HeroSection() {

  /* typing animation */
  const [typed, setTyped] = useState("");
  const text = "quantum_qnn.train(dataset)";
  const indexRef = useRef(0);

  useEffect(() => {
    const typing = setInterval(() => {

      if (indexRef.current < text.length) {
        setTyped(text.slice(0, indexRef.current + 1));
        indexRef.current++;
      } else {
        setTimeout(() => {
          indexRef.current = 0;
          setTyped("");
        }, 2000);
      }

    }, 80);

    return () => clearInterval(typing);
  }, []);

  /* smooth scroll */
 // Définir la fonction dans HeroSection
const scrollToResearch = () => {
  const element = document.getElementById("final-cta"); // ID de la section cible
  if (element) {
    element.scrollIntoView({ behavior: "smooth" }); // Scroll fluide
  }
};

  return (
    <section className="relative min-h-screen flex items-center overflow-hidden quantum-grid">

      {/* Background gradients */}
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-1/4 left-1/3 w-96 h-96 rounded-full"
          style={{ background: "radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%)" }}
        />
        <div
          className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full"
          style={{ background: "radial-gradient(circle, rgba(6,182,212,0.10) 0%, transparent 70%)" }}
        />
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full"
          style={{ background: "radial-gradient(circle, rgba(16,207,170,0.05) 0%, transparent 70%)" }}
        />
      </div>

      <div className="max-w-7xl mx-auto px-6 pt-32 pb-20 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center w-full">

        {/* LEFT SIDE */}
        <div className="relative z-10">

          {/* badge */}
          <div className="inline-flex items-center gap-2 glass px-4 py-2 rounded-full mb-8 animate-fadeInUp">
            <span className="w-2 h-2 rounded-full bg-quantum-teal animate-pulse-glow" />
            <span className="font-mono text-xs text-quantum-teal tracking-widest uppercase">
              Quantum ML Research Platform
            </span>
          </div>

          {/* headline */}
          <h1
            className="font-mono font-black leading-[0.9] mb-6 animate-fadeInUp delay-100"
            style={{ fontSize: "clamp(2.8rem, 6vw, 5.5rem)" }}
          >
            <span className="block text-text-primary">Beyond</span>
            <span className="block gradient-text">Classical</span>
            <span className="block text-text-primary">Neural Nets.</span>
          </h1>

          {/* description */}
          <p className="font-sans text-lg text-text-secondary max-w-xl leading-relaxed mb-8 animate-fadeInUp delay-200">
            Automatically compare your classical RNNs with quantum QNNs —
            no quantum computing expertise required. Upload, train, visualize, export.
          </p>

          {/* terminal */}
          <div className="glass rounded-xl p-4 mb-10 font-mono text-sm max-w-md animate-fadeInUp delay-300">

            <div className="flex items-center gap-2 mb-3">
              <span className="w-3 h-3 rounded-full bg-red-500/70" />
              <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
              <span className="w-3 h-3 rounded-full bg-green-500/70" />
              <span className="text-xs text-text-muted ml-2 tracking-widest">
                neurospace_cli
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-quantum-teal">›</span>
              <span className="text-text-secondary">{typed}</span>
              <span className="w-2 h-4 bg-quantum-cyan animate-blink" />
            </div>

          </div>

          {/* CTA buttons */}
          <div className="flex flex-wrap items-center gap-4 animate-fadeInUp delay-400">

           <button
  onClick={scrollToResearch}
  className="btn-quantum px-8 py-4 rounded-xl text-sm font-mono font-semibold relative z-10"
>
  <span className="relative z-10">
    View documentation →
  </span>
</button>
            <Link
              href="/sign-up-login"
              className="btn-outline px-8 py-4 rounded-xl text-sm font-mono font-semibold"
            >
              Create Account
            </Link>

          </div>

          {/* trust indicators */}
          <div className="flex items-center gap-6 mt-10 animate-fadeInUp delay-500">

            {[
              { val: "5-qubit", label: "QNN" },
              { val: "Auto", label: "Pipeline" },
              { val: "JSON/PDF", label: "Export" },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <div className="font-mono font-bold text-quantum-cyan text-lg">
                  {s.val}
                </div>
                <div className="font-mono text-[10px] text-text-muted uppercase tracking-widest">
                  {s.label}
                </div>
              </div>
            ))}

          </div>

        </div>

        {/* RIGHT SIDE */}
        <div className="relative hidden lg:block">

          {/* quantum circuit panel */}
          <div className="glass rounded-2xl p-6 relative overflow-hidden scan-overlay">

            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-xs text-text-muted uppercase tracking-widest">
                QNN Circuit — Live Preview
              </span>

              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-quantum-teal animate-pulse" />
                <span className="font-mono text-[10px] text-quantum-teal">
                  ACTIVE
                </span>
              </div>
            </div>

            <div className="h-64">
              <QuantumCircuitSVG />
            </div>

            <div className="mt-4 grid grid-cols-3 gap-3">
              {[
                { label: "Qubits", value: "5" },
                { label: "Gates", value: "24" },
                { label: "Depth", value: "12" },
              ].map((m) => (
                <div
                  key={m.label}
                  className="bg-panel/50 rounded-lg p-2 text-center"
                >
                  <div className="font-mono font-bold text-quantum-cyan text-lg">
                    {m.value}
                  </div>
                  <div className="font-mono text-[10px] text-text-muted">
                    {m.label}
                  </div>
                </div>
              ))}
            </div>

          </div>

          {/* floating metrics */}
          {floatingCards.map((card) => (

            <div
              key={card.label}
              className={`absolute glass-cyan rounded-xl p-3 w-44 ${card.style} z-10`}
            >

              <div className="flex items-center gap-2 mb-1">
                <span>{card.icon}</span>
                <span className="font-mono text-[10px] text-text-muted uppercase tracking-wider">
                  {card.label}
                </span>
              </div>

              <div
                className={`font-mono font-bold text-xl ${
                  card.color === "cyan"
                    ? "text-quantum-cyan"
                    : card.color === "purple"
                    ? "text-quantum-violet"
                    : "text-quantum-teal"
                }`}
              >
                {card.value}
              </div>

              <div className="font-mono text-[10px] text-quantum-teal mt-0.5">
                {card.delta}
              </div>

            </div>

          ))}

        </div>

      </div>

      {/* scroll indicator */}
      <div
        onClick={scrollToResearch}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-float cursor-pointer"
      >
        <span className="font-mono text-[10px] text-text-muted tracking-widest uppercase">
          Scroll
        </span>

        <div className="w-5 h-8 rounded-full border border-quantum-purple/30 flex items-start justify-center p-1">
          <div className="w-1 h-2 rounded-full bg-quantum-cyan animate-float" />
        </div>
      </div>

    </section>
  );
}