import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Privacy Policy | NeuroSpace",
  description: "Privacy Policy for the NeuroSpace quantum ML platform.",
};

const sections = [
  {
    title: "Introduction",
    body: [
      "This Privacy Policy explains, in general terms, how NeuroSpace may collect, use, store, and process information when you use the platform.",
      "NeuroSpace is an experimental academic and research SaaS platform for comparing classical and quantum machine learning models on numerical tabular classification datasets. This policy is an informational template and is not legal advice.",
    ],
  },
  {
    title: "Data We Collect",
    body: [
      "NeuroSpace may collect account information, authentication information, uploaded datasets, training configurations, generated results, report files, payment-related records, and technical usage data needed to operate the platform.",
      "The exact data collected may depend on the features you use, the plan you select, and the third-party services involved in authentication, hosting, storage, processing, and payments.",
    ],
  },
  {
    title: "Authentication Data",
    body: [
      "When you create an account or sign in, NeuroSpace may process your email address, user identifier, display name, institution, and authentication metadata.",
      "If you use Google Authentication, Google may provide basic account information needed to authenticate you. Google handles the authentication process according to its own policies.",
    ],
  },
  {
    title: "Uploaded Datasets",
    body: [
      "Uploaded datasets may be stored and processed so NeuroSpace can validate files, run training jobs, compare models, and generate outputs.",
      "You should only upload datasets that you are authorized to use. NeuroSpace is intended for numerical tabular classification data and is not intended for unnecessary sensitive personal information.",
    ],
  },
  {
    title: "Training Configurations and Results",
    body: [
      "NeuroSpace may store configuration settings such as model choices, training parameters, selected targets, job status, metrics, and result summaries.",
      "These records help the platform display dashboards, resume workflows, compare experiments, and support generated reports.",
    ],
  },
  {
    title: "Generated PDF and JSON Reports",
    body: [
      "PDF and JSON reports may include dataset metadata, model settings, metrics, charts, summaries, and analysis generated from your training jobs.",
      "Reports may be stored or made available for download depending on platform functionality and your account permissions.",
    ],
  },
  {
    title: "Payment Information",
    body: [
      "Payment information may be processed by third-party payment providers such as PayPal. NeuroSpace may store payment status, plan, invoice identifiers, amount, currency, and related account metadata.",
      "NeuroSpace should not store full payment card details unless a properly authorized payment provider or compliant integration is used for that purpose.",
    ],
  },
  {
    title: "Third-Party Services Used",
    body: [
      "NeuroSpace may use Supabase for authentication, database, storage, and related backend services; Vercel for frontend hosting; Render for backend hosting; Google Authentication for sign-in; and PayPal for payment processing.",
      "These providers may process data according to their own terms, privacy notices, infrastructure practices, and security controls.",
    ],
  },
  {
    title: "Data Storage and Security",
    body: [
      "NeuroSpace aims to use reasonable technical and organizational safeguards appropriate for an experimental research SaaS platform, such as access controls, provider security features, and controlled service integrations.",
      "No online platform can guarantee absolute security. Users should avoid uploading highly sensitive data unless they have assessed the risks and confirmed the platform is appropriate for that use.",
    ],
  },
  {
    title: "User Responsibilities",
    body: [
      "You are responsible for the legality, quality, and sensitivity of data you upload, as well as for maintaining backups of important datasets and reports.",
      "You should ensure your use of NeuroSpace aligns with your institution's policies, research ethics requirements, data sharing rules, and any laws that may apply to your datasets.",
    ],
  },
  {
    title: "Data Retention",
    body: [
      "NeuroSpace may retain account records, uploaded files, training jobs, reports, and payment records for as long as needed to provide the service, support user workflows, maintain security, resolve disputes, or meet operational requirements.",
      "Data deletion and retention behavior may depend on account settings, subscription state, infrastructure providers, backup schedules, and administrative processes.",
    ],
  },
  {
    title: "Contact",
    body: [
      "For privacy questions, deletion requests, or data handling concerns, contact the NeuroSpace team through the support or contact channel provided in the application.",
      "Current platform URL: https://neuro-space-teal.vercel.app",
    ],
  },
];

export default function PrivacyPolicyPage() {
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
              Privacy Policy
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-text-secondary sm:text-base">
              A clear overview of the data NeuroSpace may collect and process
              while supporting authentication, datasets, training workflows,
              reports, hosting, and payments.
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
