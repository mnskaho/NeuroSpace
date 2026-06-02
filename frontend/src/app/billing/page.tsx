"use client";

import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function BillingPage() {
  const router = useRouter();
  const [payments, setPayments] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      const { data } = await supabase
        .from("payments")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", { ascending: false });

      setPayments(data || []);
    };

    load();
  }, []);

  const viewInvoice = (payment: any) => {
    router.push(`/invoice/${payment.id}`);
  };

  return (
    <div className="p-8 max-w-5xl mx-auto relative">
      {/* Back Button fixe à gauche */}
      <div className="fixed top-4 left-4 z-50">
  <button
    onClick={() => router.push("/payment-success")}
    className="flex items-center gap-2 text-xs font-semibold text-text-primary px-4 py-2 rounded-lg glass-cyan border border-cyan-400 transition shadow-md hover:shadow-cyan-500/60 hover:scale-105 hover:text-accent-cyan"
  >
    Back
  </button>
</div>
      <h1 className="text-3xl font-bold mb-6">Billing & Invoices</h1>

      <div className="bg-gray-900 rounded-2xl p-6">
        <table className="w-full text-left">
          <thead className="text-gray-400">
            <tr>
              <th>Invoice</th>
              <th>Date</th>
              <th>Amount</th>
              <th>Method</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {payments.map((p) => (
              <tr key={p.id} className="border-t border-gray-700">
                <td>{p.invoice_number}</td>
                <td>{new Date(p.created_at).toLocaleDateString()}</td>
                <td>{p.amount} €</td>
                <td>{p.payment_method}</td>
                <td>
                  <button
                    onClick={() => viewInvoice(p)}
                    className="px-3 py-1 bg-cyan-500 text-black rounded hover:bg-cyan-600"
                  >
                    View Invoice
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}