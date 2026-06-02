"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import AppLogo from "@/components/ui/AppLogo";
import Icon from "@/components/ui/AppIcon";

const navLinks = [
  { label: "Platform", href: "/homepage#platform" },
  { label: "Pipeline", href: "/homepage#pipeline" },
  { label: "Research", href: "/homepage#research" },
];

export default function Header() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const isDashboard = pathname === "/dashboard";

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled || isDashboard
          ? "bg-space/95 backdrop-blur-xl border-b border-quantum-purple/10 shadow-card"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/homepage" className="flex items-center gap-3 group">
  <AppLogo size={70} />

  <div className="flex flex-col">
    <span
      className="text-xl font-bold tracking-tight"
      style={{ fontFamily: "Manrope, sans-serif" }}
    >
      Neuro
      <span className="gradient-text-violet font-display italic font-semibold">
        Space
      </span>
    </span>

    <span className="font-mono text-[10px] text-text-muted tracking-widest uppercase">
      Quantum ML
    </span>
  </div>
</Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
  {navLinks?.map((link) => (
    <Link
      key={link?.label}
      href={link?.href}
      className="font-mono text-sm text-text-secondary hover:text-quantum-cyan transition-colors tracking-widest uppercase"
    >
      {link?.label}
    </Link>
  ))}
</nav>

        {/* CTA */}
        <div className="hidden md:flex items-center gap-3">
         
          <Link
            href="/sign-up-login"
            className="btn-quantum font-mono text-xs px-5 py-2.5 rounded-lg"
          >
            <span>Sign In</span>
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className="md:hidden p-2 text-text-secondary hover:text-text-primary transition-colors"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle menu"
        >
          <Icon name={mobileOpen ? "XMarkIcon" : "Bars3Icon"} size={22} />
        </button>
      </div>
      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden glass border-t border-quantum-purple/10 px-6 py-4 flex flex-col gap-4">
          {navLinks?.map((link) => (
            <Link
              key={link?.label}
              href={link?.href}
              className="font-mono text-sm text-text-secondary hover:text-quantum-cyan transition-colors"
              onClick={() => setMobileOpen(false)}
            >
              {link?.label}
            </Link>
          ))}
          <div className="flex flex-col gap-3 pt-2 border-t border-quantum-purple/10">
            <Link href="/sign-up-login" className="btn-outline font-mono text-xs px-5 py-2.5 rounded-lg text-center">
              Sign In
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}