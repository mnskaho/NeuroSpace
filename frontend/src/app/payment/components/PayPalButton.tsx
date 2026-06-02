"use client";

import { useEffect, useRef, useCallback } from "react";
import { toast } from "react-hot-toast";

declare global {
  interface Window {
    paypal: any;
  }
}

interface PayPalButtonProps {
  amount: number;
  plan: string;
  onSuccess: () => Promise<void> | void;
}

export default function PayPalButton({
  amount,
  plan,
  onSuccess,
}: PayPalButtonProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  // 🔹 Stable function (évite re-render PayPal SDK)
  const handleSuccess = useCallback(async () => {
    try {
      await onSuccess();
    } catch (err) {
      console.error("onSuccess error:", err);
    }
  }, [onSuccess]);

  useEffect(() => {
    if (!containerRef.current) return;
    if (amount <= 0) return;

    let isMounted = true;

    const loadPayPalScript = () => {
      return new Promise<void>((resolve, reject) => {
        if (document.getElementById("paypal-sdk")) return resolve();

        const script = document.createElement("script");
        script.id = "paypal-sdk";
        script.src = `https://www.paypal.com/sdk/js?client-id=${process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID}&currency=EUR&intent=capture`;
        script.async = true;

        script.onload = () => resolve();
        script.onerror = () => reject("PayPal SDK failed to load");

        document.body.appendChild(script);
      });
    };

    const renderButtons = () => {
      if (!isMounted || !window.paypal || !containerRef.current) return;

      containerRef.current.innerHTML = "";

      window.paypal
        .Buttons({
          style: {
            layout: "vertical",
            color: "blue",
            shape: "rect",
            label: "paypal",
          },

          createOrder: async () => {
            try {
              const res = await fetch("/api/paypal/create-order", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({ plan }),
              });

              const data = await res.json();

              if (!res.ok || !data?.id) {
                throw new Error("Invalid PayPal order response");
              }

              return data.id;
            } catch (err) {
              console.error("createOrder error:", err);
              toast.error("Failed to create order ❌");
              throw err;
            }
          },

          onApprove: async (data: any) => {
            try {
              const res = await fetch("/api/paypal/capture-order", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({ orderID: data.orderID }),
              });

              const details = await res.json();

              if (!res.ok || details?.error) {
                toast.error("Payment failed ❌");
                return;
              }

              toast.success("Payment successful ✅");
              await handleSuccess();
            } catch (err) {
              console.error("capture error:", err);
              toast.error("Payment error ❌");
            }
          },

          onCancel: () => {
            toast("Payment cancelled ❌");
            console.warn("User closed PayPal popup");
          },

          onError: (err: any) => {
            console.error("PayPal error:", err);
            toast.error("PayPal error ❌");
          },
        })
        .render(containerRef.current);
    };

    loadPayPalScript()
      .then(renderButtons)
      .catch((err) => {
        console.error(err);
        toast.error("PayPal SDK failed to load ❌");
      });

    return () => {
      isMounted = false;
    };
  }, [amount, plan, handleSuccess]);

  return <div ref={containerRef} />;
}


// "use client";
// import { toast } from "react-hot-toast";
// import { useEffect, useRef } from "react";

// declare global {
//   interface Window {
//     paypal: any;
//   }
// }


// interface PayPalButtonProps {
//   amount: number;
//   plan: string; // 🔥
//   onSuccess: () => Promise<void>;
// }

// export default function PayPalButton({ amount, plan, onSuccess }: PayPalButtonProps) {
//   const containerRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     if (!containerRef.current) return;

//     // 🔹 Interception du warning PayPal spécifique
//     const originalConsoleError = console.error;
//     console.error = (...args: any[]) => {
//       if (
//         typeof args[0] === "string" &&
//         args[0].includes("paypal_js_sdk_v5_unhandled_exception")
//       ) {
//         return; // ignore ce warning spécifique
//       }
//       originalConsoleError(...args);
//     };

//     // Charge le script PayPal si pas déjà présent
//     if (!document.getElementById("paypal-sdk")) {
//       const script = document.createElement("script");
//       script.id = "paypal-sdk";
//       script.src = `https://www.paypal.com/sdk/js?client-id=${process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID}&currency=EUR&intent=capture`;
//       script.async = true;

//       script.onload = () => renderPayPalButtons();
//       script.onerror = (err) => console.error("PayPal SDK load error:", err);

//       document.body.appendChild(script);
//     } else {
//       renderPayPalButtons();
//     }

//     function renderPayPalButtons() {
//       if (!window.paypal || !containerRef.current) {
//         console.warn("PayPal SDK not loaded yet");
//         return;
//       }

//       // Nettoie les anciens boutons
//       containerRef.current.innerHTML = "";

//       if (amount <= 0) {
//         console.warn("PayPal amount invalid:", amount);
//         return;
//       }

//       window.paypal
//         .Buttons({
//           style: {
//             layout: "vertical",
//             color: "blue",
//             shape: "rect",
//             label: "paypal",
//           },

//           // createOrder: async (data: any, actions: any) => {
//           //   try {
//           //     return await actions.order.create({
//           //       purchase_units: [{ amount: { value: amount.toFixed(2) } }],
//           //     });
//           //   } catch (err) {
//           //     console.error("PayPal createOrder error:", err);
//           //     alert("Failed to create PayPal order ❌");
//           //     throw err;
//           //   }
//           // },

//             createOrder: async () => {
//   const res = await fetch("/api/paypal/create-order", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json", // ✅ AJOUT ICI
//     },
//     body: JSON.stringify({ plan }), // ✅ utiliser le vrai plan
//   });

//   const data = await res.json();
//   return data.id;
// },

//           // onApprove: async (data: any, actions: any) => {
//           //   try {
//           //     const details = await actions.order.capture();
//           //     console.log("PayPal payment completed:", details);

//           //     // Appelle la fonction passée depuis PaymentPage
//           //     await onSuccess();
//           //   } catch (err) {
//           //     console.error("PayPal capture error:", err);
//           //     alert("Payment capture failed ❌");
//           //   }
//           // },

//           onApprove: async (data: any) => {
//   const res = await fetch("/api/paypal/capture-order", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json", // ✅ ICI
//     },
//     body: JSON.stringify({ orderID: data.orderID }),
//   });

//   const details = await res.json();

//   if (details.error) {
//     toast.error("Payment failed ❌");
//     return;
//   }

//   await onSuccess();
// },

//           onCancel: (data: any) => {
//             console.warn("PayPal payment cancelled:", data);
//             toast("Payment cancelled ❌");
//           },

//           onError: (err: any) => {
//             console.error("PayPal SDK error:", err);
//             toast.error("Payment failed ❌");
//           },
//         })
//         .render(containerRef.current);
//     }

//     return () => {
//       console.error = originalConsoleError; // restore original console.error
//     };
//   }, [amount, onSuccess]);

//   return <div ref={containerRef} />;
// }


