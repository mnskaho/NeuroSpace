"use client";

import emailjs from "@emailjs/browser";
import { useState } from "react";
import Link from "next/link";
import {
  BookOpenIcon,
  QuestionMarkCircleIcon,
  EnvelopeIcon,
  ChevronDownIcon,
  ArrowTopRightOnSquareIcon,
  ChevronLeftIcon, // <-- ajouté pour le bouton Back
} from "@heroicons/react/24/outline";

import { useRouter } from "next/navigation"; // <-- ajouté pour router.back()

interface FAQ {
  question: string;
  answer: string;
}

export default function SupportPage() {
  const [faqOpen, setFaqOpen] = useState(false);
  const [activeQuestion, setActiveQuestion] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);
  
   const router = useRouter();

  const faqs: FAQ[] = [
    {
      question: "How do I update my profile information?",
      answer: "Go to your profile page and click 'Edit Profile'. Update your information and save changes."
    },
    {
      question: "How do I change my password?",
      answer: "Open Settings → Security → Change password and enter your new password."
    },
    {
      question: "How do I enable dark mode?",
      answer: "Go to Settings → Appearance and toggle Dark Mode."
    },
    {
      question: "How do I manage email notifications?",
      answer: "Navigate to Settings → Notifications and enable or disable email alerts."
    },
    {
      question: "How do I log out securely?",
      answer: "Click the Logout button from the sidebar or profile menu."
    }
  ];

  const toggleQuestion = (index: number) => {
    setActiveQuestion(activeQuestion === index ? null : index);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (message.length < 20) {
      alert("Message must contain at least 20 characters");
      return;
    }
    const form = e.target as HTMLFormElement;

    emailjs.sendForm(
      "service_vbq56nq", // ton Service ID
      "template_i6hxh3i", // ton Template ID
      form,
      "1vLjiwlyelUJaGfMz" // ta Public Key
    ).then(
      (result) => {
        console.log(result.text);
        setSubmitted(true);
        setMessage("");
      },
      (error) => {
        console.log(error.text);
        alert("Failed to send message. Please try again.");
      }
    );
  };

  const handleReset = () => {
    setMessage("");
    setSubmitted(false);
  };

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-8">

      {/* BACK BUTTON - STICKY */}
      <div className="sticky top-4 left-4 z-50">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
        >
          Back
        </button>
      </div>


      {/* HERO */}
      <div className="glass rounded-xl p-8 flex items-center justify-between">
        <div className="flex gap-4 items-center">
          <div className="w-14 h-14 rounded-xl flex items-center justify-center bg-gradient-to-br from-purple-500 to-cyan-500">
            <QuestionMarkCircleIcon className="w-7 h-7 text-white"/>
          </div>
          <div>
            <h1 className="text-2xl font-semibold">How can we help you?</h1>
            <p className="text-text-secondary text-sm">
              Browse our resources or contact our support team. We typically respond within 24 hours.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 bg-green-500/10 px-4 py-2 rounded-lg">
          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
          <span className="text-sm text-green-400">Support Online</span>
        </div>
      </div>

      {/* HELP RESOURCES */}
      <div className="glass rounded-xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <BookOpenIcon className="w-6 h-6 text-cyan-400"/>
          <div>
            <h2 className="text-lg font-semibold">Help Resources</h2>
            <p className="text-sm text-text-secondary">Quick access to guides and documentation</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {/* FAQ CARD */}
          <button
            onClick={() => setFaqOpen(!faqOpen)}
            className="glass-cyan p-5 rounded-xl flex justify-between items-start hover:border-cyan-400 transition"
          >
            <div className="flex gap-3">
              <div className="w-10 h-10 rounded-lg bg-yellow-400/10 flex items-center justify-center">
                <QuestionMarkCircleIcon className="w-5 h-5 text-yellow-400"/>
              </div>
              <div className="text-left">
                <p className="font-medium">Frequently Asked Questions</p>
                <p className="text-sm text-text-secondary">Find answers to common questions</p>
              </div>
            </div>
            <ChevronDownIcon
              className={`w-5 transition-transform duration-300 ${faqOpen ? "rotate-180" : ""}`}
            />
          </button>

          {/* DOC CARD */}
         {/* DOC CARD */}
<Link
  href="/documentation"
  className="glass-cyan p-5 rounded-xl flex justify-between items-start hover:border-purple-500 transition cursor-pointer"
>
  <div className="flex gap-3">
    <div className="w-10 h-10 rounded-lg bg-cyan-500/10 flex items-center justify-center">
      <BookOpenIcon className="w-5 h-5 text-cyan-400" />
    </div>
    <div>
      <p className="font-medium">Documentation</p>
      <p className="text-sm text-text-secondary">Guides and API references</p>
    </div>
  </div>
  <ArrowTopRightOnSquareIcon className="w-4 text-text-secondary" />
</Link>
        </div>

        {/* FAQ LIST */}
        {faqOpen && (
          <div className="mt-6 space-y-3">
            {faqs.map((faq, index) => {
              const isOpen = activeQuestion === index;
              return (
                <div key={index} className="glass rounded-lg overflow-hidden border border-border">
                  <button
                    onClick={() => toggleQuestion(index)}
                    className="w-full flex justify-between items-center px-5 py-4 hover:bg-white/5 transition"
                  >
                    <span className="text-sm font-medium">{faq.question}</span>
                    <ChevronDownIcon
                      className={`w-5 transition-transform duration-300 ${isOpen ? "rotate-180 text-cyan-400" : "text-text-secondary"}`}
                    />
                  </button>
                  <div className={`grid transition-all duration-300 ${isOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"}`}>
                    <div className="overflow-hidden">
                      <p className="px-5 pb-5 text-sm text-text-secondary leading-relaxed">{faq.answer}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* CONTACT FORM */}
      <div className="glass rounded-xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <EnvelopeIcon className="w-6 text-green-400"/>
          <div>
            <h2 className="text-lg font-semibold">Contact Support</h2>
            <p className="text-text-secondary text-sm">We'll get back to you within 24 hours</p>
          </div>
        </div>

        {submitted && (
          <div className="mb-4 bg-green-500/10 text-green-400 p-3 rounded-lg text-sm">
            Message sent successfully!
          </div>
        )}

        <form onSubmit={handleSubmit} className="grid md:grid-cols-2 gap-4">
          <input name="from_name" className="input-quantum p-3 rounded-lg" placeholder="Full name" required />
          <input name="from_email" type="email" className="input-quantum p-3 rounded-lg" placeholder="Email address" required />
          <select name="category" className="input-quantum p-3 rounded-lg">
            <option>Select category</option>
            <option>Account</option>
            <option>Technical issue</option>
            <option>Security</option>
            <option>Feature request</option>
          </select>
          <select name="priority" className="input-quantum p-3 rounded-lg">
            <option>Select priority</option>
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
            <option>Critical</option>
          </select>
          <input name="subject" className="input-quantum p-3 rounded-lg md:col-span-2" placeholder="Subject" required />
          <div className="md:col-span-2">
            <textarea
              name="message"
              className="input-quantum w-full p-3 rounded-lg h-32"
              placeholder="Describe your issue..."
              value={message}
              maxLength={1000}
              onChange={(e) => setMessage(e.target.value)}
            />
            <div className="text-right text-xs text-text-muted mt-1">{message.length} / 1000</div>
          </div>
          <div className="flex gap-3 md:col-span-2 mt-2">
            <button type="reset" onClick={handleReset} className="btn-outline px-5 py-2 rounded-lg">Reset</button>
            <button type="submit" className="px-6 py-2 rounded-lg bg-cyan-500 text-white font-medium shadow-sm hover:bg-cyan-600 hover:shadow-md transition-all">Send Message</button>
          </div>
        </form>
      </div>

      {/* OTHER WAYS TO REACH US */}
      <div className="glass rounded-xl p-6">
        <h3 className="text-lg font-semibold mb-6">Other Ways to Reach Us</h3>
        <div className="grid md:grid-cols-3 gap-6">
          {/* Email */}
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-purple-500/10">
              <EnvelopeIcon className="w-5 text-purple-400"/>
            </div>
            <div>
              <p className="text-xs text-text-muted">Email</p>
              <p className="text-sm font-medium">mnskaho@gmail.com</p>
            </div>
          </div>
          {/* Response Time */}
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-cyan-500/10">
              <span className="text-cyan-400 text-lg">⏱</span>
            </div>
            <div>
              <p className="text-xs text-text-muted">Response Time</p>
              <p className="text-sm font-medium">Within 24 hours</p>
            </div>
          </div>
          {/* Availability */}
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-green-500/10">
              <span className="text-green-400 text-lg">🕒</span>
            </div>
            <div>
              <p className="text-xs text-text-muted">Availability</p>
              <p className="text-sm font-medium">Sun–Thu, 9AM–7PM CET</p>
            </div>
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <div className="text-center text-sm text-text-muted py-4">
        © 2026 NeuroSpace All Rights Reserved. | <Link href="/dashboard" className="text-cyan-500 hover:underline">Dashboard</Link> | <Link href="/settings" className="text-cyan-500 hover:underline">Settings</Link>
      </div>

    </div>
  );
}