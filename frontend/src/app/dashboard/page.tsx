import type { Metadata } from "next";
import DashboardInteractive from "./components/DashboardInteractive";

export const metadata: Metadata = {
  title: "Dashboard — NeuroSpace",
  description: "Quantum RNN research pipeline: upload, train, evaluate, and visualize classical vs QNN models.",
};

export default function DashboardPage() {
  return <DashboardInteractive />;
}