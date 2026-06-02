"use client";

import { useEffect, useRef } from "react";

export default function QuantumCircuitSVG() {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    const lines = svgRef.current?.querySelectorAll(".qubit-line");
    const gates = svgRef.current?.querySelectorAll(".gate");
    
    lines?.forEach((line, i) => {
      (line as SVGElement).style.animationDelay = `${i * 0.4}s`;
    });
    gates?.forEach((gate, i) => {
      (gate as SVGElement).style.animationDelay = `${i * 0.15}s`;
    });
  }, []);

  return (
    <svg
      ref={svgRef}
      viewBox="0 0 520 320"
      className="w-full h-full"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#7C3AED" stopOpacity="0.2" />
          <stop offset="50%" stopColor="#06B6D4" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#10CFAA" stopOpacity="0.2" />
        </linearGradient>
        <linearGradient id="gateGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#7C3AED" />
          <stop offset="100%" stopColor="#06B6D4" />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <filter id="glow-soft">
          <feGaussianBlur stdDeviation="6" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Background subtle grid */}
      <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(124,58,237,0.08)" strokeWidth="0.5" />
      </pattern>
      <rect width="520" height="320" fill="url(#grid)" />

      {/* Qubit labels */}
      {[60, 110, 160, 210, 260].map((y, i) => (
        <g key={i}>
          <text x="12" y={y + 5} fill="#8B9CC8" fontSize="11" fontFamily="JetBrains Mono" fontWeight="500">
            |q{i}⟩
          </text>
          {/* Main qubit lines */}
          <line
            className="qubit-line"
            x1="55" y1={y} x2="480" y2={y}
            stroke="url(#lineGrad)"
            strokeWidth="1.5"
            strokeOpacity="0.6"
            style={{ animation: `circuit-pulse ${2 + i * 0.3}s ease-in-out infinite` }}
          />
        </g>
      ))}

      {/* H Gates */}
      {[60, 110, 160].map((y, i) => (
        <g key={i} filter="url(#glow)">
          <rect
            className="gate"
            x={68 + i * 2} y={y - 12}
            width="24" height="24"
            rx="4"
            fill="url(#gateGrad)"
            fillOpacity="0.9"
            style={{ animation: `pulse-glow ${1.5 + i * 0.2}s ease-in-out infinite` }}
          />
          <text x={75 + i * 2} y={y + 5} fill="white" fontSize="10" fontFamily="JetBrains Mono" fontWeight="700">H</text>
        </g>
      ))}

      {/* CNOT Gates (control-target pairs) */}
      <g filter="url(#glow)">
        {/* Control dot q0 → q1 */}
        <circle cx="145" cy="60" r="5" fill="#06B6D4" style={{ animation: 'pulse-glow 2s ease-in-out infinite 0.3s' }} />
        <line x1="145" y1="65" x2="145" y2="98" stroke="#06B6D4" strokeWidth="1.5" strokeOpacity="0.7" />
        <circle cx="145" cy="110" r="10" fill="none" stroke="#06B6D4" strokeWidth="2" />
        <line x1="135" y1="110" x2="155" y2="110" stroke="#06B6D4" strokeWidth="1.5" />
        <line x1="145" y1="100" x2="145" y2="120" stroke="#06B6D4" strokeWidth="1.5" />
      </g>

      <g filter="url(#glow)">
        {/* Control dot q1 → q2 */}
        <circle cx="195" cy="110" r="5" fill="#7C3AED" style={{ animation: 'pulse-glow 2.2s ease-in-out infinite 0.6s' }} />
        <line x1="195" y1="115" x2="195" y2="148" stroke="#7C3AED" strokeWidth="1.5" strokeOpacity="0.7" />
        <circle cx="195" cy="160" r="10" fill="none" stroke="#7C3AED" strokeWidth="2" />
        <line x1="185" y1="160" x2="205" y2="160" stroke="#7C3AED" strokeWidth="1.5" />
        <line x1="195" y1="150" x2="195" y2="170" stroke="#7C3AED" strokeWidth="1.5" />
      </g>

      {/* RZ Rotation gates */}
      {[210, 260].map((y, i) => (
        <g key={i} filter="url(#glow)">
          <rect x={240 + i * 5} y={y - 12} width="30" height="24" rx="4"
            fill="none" stroke="#10CFAA" strokeWidth="1.5"
            style={{ animation: `pulse-glow ${1.8 + i * 0.3}s ease-in-out infinite 0.4s` }}
          />
          <text x={244 + i * 5} y={y + 5} fill="#10CFAA" fontSize="9" fontFamily="JetBrains Mono" fontWeight="600">Rz</text>
        </g>
      ))}

      {/* Measurement symbols */}
      {[60, 110, 160, 210, 260].map((y, i) => (
        <g key={i} filter="url(#glow)">
          <rect x="430" y={y - 14} width="28" height="28" rx="4"
            fill="rgba(124,58,237,0.15)" stroke="rgba(124,58,237,0.5)" strokeWidth="1"
          />
          {/* Meter arc */}
          <path
            d={`M ${436} ${y + 6} A 8 8 0 0 1 ${452} ${y + 6}`}
            fill="none" stroke="#A78BFA" strokeWidth="1.5"
          />
          <line x1="444" y1={y + 6} x2="450" y2={y - 2} stroke="#A78BFA" strokeWidth="1.5" />
        </g>
      ))}

      {/* Flowing data particles */}
      {[60, 160, 260].map((y, i) => (
        <circle key={i} r="3" fill="#06B6D4" filter="url(#glow)">
          <animateMotion
            dur={`${2 + i * 0.5}s`}
            repeatCount="indefinite"
            begin={`${i * 0.7}s`}
          >
            <mpath href="#qubit-path" />
          </animateMotion>
        </circle>
      ))}

      <path id="qubit-path" d="M 55 160 L 480 160" fill="none" />

      {/* Entanglement arcs */}
      <path
        d="M 145 60 Q 170 85 145 110"
        fill="none" stroke="rgba(6,182,212,0.3)" strokeWidth="1" strokeDasharray="4 3"
        style={{ animation: 'circuit-pulse 3s ease-in-out infinite' }}
      />

      {/* Labels */}
      <text x="68" y="295" fill="#4B5A7A" fontSize="9" fontFamily="JetBrains Mono">Encoding Layer</text>
      <text x="165" y="295" fill="#4B5A7A" fontSize="9" fontFamily="JetBrains Mono">Entanglement</text>
      <text x="270" y="295" fill="#4B5A7A" fontSize="9" fontFamily="JetBrains Mono">Rotation</text>
      <text x="430" y="295" fill="#4B5A7A" fontSize="9" fontFamily="JetBrains Mono">Measure</text>

      {/* Vertical separators */}
      {[155, 225, 400].map((x, i) => (
        <line key={i} x1={x} y1="40" x2={x} y2="280"
          stroke="rgba(124,58,237,0.1)" strokeWidth="1" strokeDasharray="3 4"
        />
      ))}
    </svg>
  );
}