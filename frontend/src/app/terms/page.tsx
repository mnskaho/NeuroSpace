import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Terms of Service | NeuroSpace",
  description: "Terms of Service for the NeuroSpace quantum ML platform.",
};

const sections = [
  {
    title: "Introduction",
    body: [
      "These Terms of Service describe the expected use of NeuroSpace, an experimental platform for comparing classical and quantum machine learning models on numerical tabular classification datasets.",
      "These terms are provided as an informational template for the NeuroSpace platform and are not legal advice. You should review them with a qualified legal professional before relying on them as final legal terms.",
    ],
  },
  {
    title: "Use of the Platform",
    body: [
      "NeuroSpace is designed for academic, research, educational, and exploratory SaaS use. The platform helps users upload compatible datasets, configure training jobs, compare model behavior, and review generated outputs.",
      "You agree to use the platform only for lawful purposes and in a way that does not disrupt, misuse, reverse engineer, overload, or interfere with NeuroSpace services or infrastructure.",
    ],
  },
  {
    title: "User Accounts",
    body: [
      "You are responsible for maintaining the confidentiality of your account credentials and for activity that occurs through your account.",
      "If you sign in using Google Authentication or another supported provider, your access may also be subject to that provider's terms and policies.",
    ],
  },
  {
    title: "Uploaded Datasets",
    body: [
      "You are responsible for the datasets you upload. You should only upload data that you have the right to use, process, and analyze through NeuroSpace.",
      "NeuroSpace is intended for numerical tabular classification datasets. You should avoid uploading sensitive personal data, confidential information, protected health information, or data that requires special legal handling unless you have appropriate authorization and safeguards.",
    ],
  },
  {
    title: "Training Jobs and Generated Reports",
    body: [
      "Training jobs, metrics, charts, PDF reports, JSON reports, and other generated outputs are produced from the data and configurations you provide.",
      "Generated reports are intended to support analysis and comparison. They should be reviewed by a qualified user before being used in academic work, operational decisions, publications, or business decisions.",
    ],
  },
  {
    title: "Payments and Subscriptions",
    body: [
      "Paid plans, subscriptions, or one-time purchases may provide access to additional training runs, reports, capacity, or platform features.",
      "Payment processing may be handled by third-party services such as PayPal. Prices, plan limits, billing periods, and available features may change over time and should be reviewed before purchase.",
    ],
  },
  {
    title: "Limitations of Results",
    body: [
      "NeuroSpace is experimental software. Model accuracy, runtime, metrics, quantum simulation behavior, and generated recommendations may vary depending on datasets, settings, external services, and implementation details.",
      "The platform does not guarantee scientific validity, publication readiness, business outcomes, regulatory compliance, or the suitability of any result for a specific purpose.",
    ],
  },
  {
    title: "User Responsibilities",
    body: [
      "You are responsible for validating your datasets, interpreting results carefully, maintaining backups of important data, and complying with rules that apply to your research, institution, organization, or jurisdiction.",
      "You should not use NeuroSpace to upload malicious files, infringing content, illegal material, or data that violates the rights of others.",
    ],
  },
  {
    title: "Third-Party Services",
    body: [
      "NeuroSpace may rely on third-party services for hosting, authentication, database storage, backend processing, payment processing, analytics, or delivery of platform features.",
      "Those services may have their own terms, privacy notices, uptime limitations, and security practices. NeuroSpace is not responsible for third-party services outside its reasonable control.",
    ],
  },
  {
    title: "Changes to Terms",
    body: [
      "NeuroSpace may update these terms as the platform evolves. Updates may reflect new features, provider changes, pricing changes, security practices, or operational needs.",
      "Continued use of the platform after changes are posted may indicate acceptance of the updated terms.",
    ],
  },
  {
    title: "Contact",
    body: [
      "For questions about these terms or the NeuroSpace platform, contact the NeuroSpace team through the support or contact channel provided in the application.",
      "Current platform URL: https://neuro-space-teal.vercel.app",
    ],
  },
];

export default function TermsPage() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-space text-text-primary">
      <div className="absolute inset-0 quantum-grid opacity-60" />
      <div className="absolute inset-0 bg-gradient-to-br from-quantum-purple/10 via-transparent to-quantum-cyan/10" />

      <Link
        href="/sign-up-login"
        className="absolute left-4 top-4 z-20 rounded-lg border border-quantum-cyan/30 bg-panel/70 px-4 py-2 font-mono text-xs font-semibold text-text-secondary backdrop-blur transition hover:border-quantum-cyan hover:text-quantum-cyan sm:left-6 sm:top-6"
      >
        Back
      </Link>

      <section className="relative z-10 mx-auto flex min-h-screen w-full max-w-5xl items-center px-4 py-24 sm:px-6 lg:px-8">
        <div className="glass neon-border w-full rounded-2xl p-6 shadow-card sm:p-8 lg:p-10">
          <header className="mb-10 text-center">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-quantum-cyan">
              NeuroSpace
            </p>
            <p className="mt-2 font-mono text-[11px] uppercase tracking-[0.22em] text-text-muted">
              Quantum ML Platform
            </p>
            <h1 className="gradient-text mt-6 font-display text-4xl font-semibold sm:text-5xl">
              Terms of Service
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-text-secondary sm:text-base">
              Informational terms for using NeuroSpace research workflows,
              uploaded datasets, training jobs, reports, and subscription
              features.
            </p>
          </header>

          <div className="space-y-5">
            {sections.map((section) => (
              <section
                key={section.title}
                className="rounded-xl border border-quantum-purple/20 bg-space/35 p-5"
              >
                <h2 className="mb-3 font-mono text-sm font-semibold uppercase tracking-wider text-quantum-cyan">
                  {section.title}
                </h2>
                <div className="space-y-3">
                  {section.body.map((paragraph) => (
                    <p
                      key={paragraph}
                      className="text-sm leading-7 text-text-secondary sm:text-[15px]"
                    >
                      {paragraph}
                    </p>
                  ))}
                </div>
              </section>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
