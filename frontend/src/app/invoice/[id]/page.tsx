"use client";

import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";
import { use } from "react";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface Props {
  params: Promise<{ id: string }>;
}

interface Payment {
  id: string;
  invoice_number: string;
  created_at: string;
  amount: number;
  plan: string;
  payment_method: string;
  user_name?: string;
  email: string;
}

export default function InvoicePage({ params }: Props) {
  const resolvedParams = use(params); // <-- déballer le Promise
  const { id } = resolvedParams;

  const router = useRouter();
  const [payment, setPayment] = useState<Payment | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPayment = async () => {
      try {
        const { data, error } = await supabase
          .from("payments")
          .select("*")
          .eq("id", id)
          .single();

        if (error || !data) setPayment(null);
        else setPayment(data as Payment);
      } catch (err) {
        console.error(err);
        setPayment(null);
      } finally {
        setLoading(false);
      }
    };

    fetchPayment();
  }, [id]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center text-white">
      Loading invoice...
    </div>
  );

  if (!payment) return (
    <div className="min-h-screen flex flex-col items-center justify-center text-white gap-4">
      <p>Invoice not found.</p>
       {/* BACK BUTTON */}
            <div className="sticky top-4 left-4 z-50">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
        >
          Back
        </button>
      </div>
    </div>
  );

  return (
  <div className="min-h-screen p-8 flex flex-col items-center bg-[#0a0a0f]">
    {/* Back Button fixe à gauche */}
    <div className="fixed top-4 left-4 z-50">
  <button
    onClick={() => router.push("/billing")}
    className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
  >
    Back
  </button>
</div>

      {/* Invoice Card */}
      <div className="max-w-2xl w-full bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl shadow-xl p-8 space-y-8">
        
        {/* Header */}
        <div className="flex justify-between items-center border-b border-gray-700 pb-4">
          <div>
            <h1 className="text-3xl font-bold text-white">Neuro<span className="text-cyan-400 italic">Space</span></h1>
            <p className="text-gray-400 text-sm">Invoice #{payment.invoice_number}</p>
          </div>
          <div className="text-right text-gray-300">
            <p className="font-semibold">{new Date(payment.created_at).toLocaleDateString()}</p>
            <p className="text-xs">{new Date(payment.created_at).toLocaleTimeString()}</p>
          </div>
        </div>

        {/* Client Info */}
        <div className="grid grid-cols-2 gap-4 text-sm text-gray-300">
          <div className="space-y-1">
            <p className="font-semibold text-white">{payment.user_name || payment.email}</p>
            <p className="text-gray-400 text-xs">Customer</p>
          </div>
          <div className="space-y-1">
            <p className="font-semibold">{payment.plan}</p>
            <p className="text-gray-400 text-xs">Plan</p>
          </div>
        </div>

        {/* Table Products */}
        <div className="overflow-x-auto rounded-xl border border-gray-700">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-800 text-gray-400">
              <tr>
                <th className="p-3">Product / Service</th>
                <th className="p-3 text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="bg-gray-900">
  <tr className="border-t border-gray-700 hover:bg-gray-800 transition">
    <td className="p-3">
      {payment.amount === 0
        ? "NeuroSpace Free Plan"
        : payment.amount === 150
        ? "NeuroSpace Pro Plan"
        : payment.amount === 500
        ? "NeuroSpace Pro+ Plan"
        : "NeuroSpace Premium"}
    </td>
    <td className="p-3 text-right">{payment.amount} €</td>
  </tr>
</tbody>
          </table>
        </div>

        {/* Total */}
        <div className="flex justify-end text-white">
          <div className="w-48 space-y-1">
            <div className="flex justify-between">
              <span>Subtotal</span>
              <span>{payment.amount} €</span>
            </div>
            <div className="flex justify-between">
              <span>Tax</span>
              <span>0 €</span>
            </div>
            <div className="flex justify-between font-bold text-lg border-t border-gray-700 pt-2">
              <span>Total</span>
              <span>{payment.amount} €</span>
            </div>
          </div>
        </div>

        {/* Payment Method */}
        <div className="text-sm text-gray-300 border-t border-gray-700 pt-4">
          <p><strong>Payment Method:</strong> {payment.payment_method}</p>
          <p><strong>Transaction ID:</strong> {payment.id}</p>
        </div>

        {/* Print Button */}
        <div>
          <button
            onClick={() => window.print()}
            className="w-full py-3 rounded-xl border border-cyan-400 text-cyan-300 hover:bg-cyan-500/10 transition"
          >
            Download / Print Invoice
          </button>
        </div>
      </div>
    </div>
  );
}
