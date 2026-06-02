"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@supabase/supabase-js";
import confetti from "canvas-confetti";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type Payment = {
  id: string;
  email: string | null;
  amount: number;
  currency: string | null;
  payment_method: string | null;
  invoice_number: string | null;
  plan: string | null;
  created_at: string;
};

export default function PaymentSuccessPage() {
  const router = useRouter();
  const [payment, setPayment] = useState<Payment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPayment = async () => {
      try {
        const {
          data: { user },
          error: userError,
        } = await supabase.auth.getUser();

        if (userError || !user) {
          setError("Please sign in to view your payment confirmation.");
          return;
        }

        const { data, error: paymentError } = await supabase
          .from("payments")
          .select("*")
          .eq("user_id", user.id)
          .order("created_at", { ascending: false })
          .limit(1)
          .maybeSingle();

        if (paymentError) throw paymentError;

        if (!data) {
          setError("No recent payment was found for your account.");
          return;
        }

        setPayment(data as Payment);
        confetti({
          particleCount: 120,
          spread: 70,
          origin: { y: 0.6 },
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not load payment confirmation.");
      } finally {
        setLoading(false);
      }
    };

    loadPayment();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen quantum-grid flex items-center justify-center bg-[#0a0a0f] px-4">
        <div className="glass rounded-2xl border border-quantum-purple/20 p-8 text-center">
          <p className="font-mono text-sm text-text-primary">Loading payment confirmation...</p>
        </div>
      </div>
    );
  }

  if (error || !payment) {
    return (
      <div className="min-h-screen quantum-grid flex items-center justify-center bg-[#0a0a0f] px-4">
        <div className="glass rounded-2xl border border-quantum-purple/20 p-8 text-center max-w-md">
          <h1 className="mb-3 text-2xl font-bold text-text-primary">Payment Confirmation</h1>
          <p className="mb-6 text-sm text-text-secondary">{error}</p>
          <button
            onClick={() => router.push("/payment")}
            className="btn-quantum rounded-xl px-6 py-3 text-sm font-semibold"
          >
            Back to Payment
          </button>
        </div>
      </div>
    );
  }

  const currency = payment.currency || "EUR";
  const amount = `${payment.amount} ${currency === "EUR" ? "EUR" : currency}`;
  const date = new Date(payment.created_at).toLocaleString();

  return (
    <div className="min-h-screen quantum-grid flex items-center justify-center bg-[#0a0a0f] px-4 py-8">
      <div className="glass neon-border w-full max-w-xl rounded-2xl p-8 space-y-6">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-500 text-3xl font-bold text-white">
            ✓
          </div>
          <h1 className="mb-2 text-3xl font-bold text-text-primary">Payment Successful</h1>
          <p className="text-sm text-text-secondary">Your purchase has been completed.</p>
        </div>

        <div className="glass-cyan rounded-xl p-5">
          <div className="mb-4 flex items-center justify-between">
            <span className="text-xs font-mono uppercase text-text-muted">Invoice</span>
            <span className="text-sm font-semibold text-text-primary">
              {payment.invoice_number || payment.id}
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4 text-sm sm:grid-cols-2">
            <div>
              <p className="text-text-muted">Plan</p>
              <p className="font-semibold text-text-primary">{payment.plan || "NeuroSpace Plan"}</p>
            </div>
            <div>
              <p className="text-text-muted">Amount</p>
              <p className="font-semibold text-text-primary">{amount}</p>
            </div>
            <div>
              <p className="text-text-muted">Method</p>
              <p className="font-semibold text-text-primary">
                {payment.payment_method || "Payment"}
              </p>
            </div>
            <div>
              <p className="text-text-muted">Date</p>
              <p className="font-semibold text-text-primary">{date}</p>
            </div>
          </div>
        </div>

        <div className="glass rounded-xl p-5">
          <p className="text-xs font-mono uppercase text-text-muted">Customer</p>
          <p className="mt-2 break-all text-sm text-text-primary">{payment.email || "-"}</p>
          <p className="mt-3 text-xs text-text-muted">Transaction ID: {payment.id}</p>
        </div>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <button
            onClick={() => router.push("/billing")}
            className="btn-outline rounded-xl px-5 py-3 text-sm font-semibold"
          >
            View Invoices
          </button>
          <button
            onClick={() => router.push("/dashboard")}
            className="btn-quantum rounded-xl px-5 py-3 text-sm font-semibold"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
