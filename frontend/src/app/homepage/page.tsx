import type { Metadata } from "next";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import HeroSection from "./components/HeroSection";
import PipelineSection from "./components/PipelineSection";
import FeaturesSection from "./components/FeaturesSection";
import StatsSection from "./components/StatsSection";

export const metadata: Metadata = {
  title: "NeuroSpace — Quantum RNN Research Platform",
  description:
    "Comparez automatiquement RNN classiques et QNN quantiques. Upload dataset, entraînement automatique, visualisation complète, export PDF/HTML.",
};

export default function HomepagePage() {
  return (
    <main className="min-h-screen bg-space">
      <Header />
      <HeroSection />
      <PipelineSection />
      <FeaturesSection />
      <StatsSection />
      <Footer />
    </main>
  );
}