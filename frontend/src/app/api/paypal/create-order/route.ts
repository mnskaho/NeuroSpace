import { NextResponse } from "next/server";

const PAYPAL_API = process.env.PAYPAL_BASE_URL!;

async function getAccessToken() {
  const auth = Buffer.from(
    `${process.env.PAYPAL_CLIENT_ID}:${process.env.PAYPAL_SECRET}`
  ).toString("base64");

  const res = await fetch(`${PAYPAL_API}/v1/oauth2/token`, {
    method: "POST",
    headers: {
      Authorization: `Basic ${auth}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
  });

  const data = await res.json();

  if (!data.access_token) {
    console.error("PayPal auth error:", data);
    throw new Error("Failed to get PayPal access token");
  }

  return data.access_token;
}

export async function POST(req: Request) {
  try {
    const { plan } = await req.json();

    const prices: Record<string, number> = {
      Pro: 150,
      "Pro+": 500,
    };

    const amount = prices[plan];

    if (!amount) {
      return NextResponse.json({ error: "Invalid plan" }, { status: 400 });
    }

    const accessToken = await getAccessToken();

    const orderRes = await fetch(`${PAYPAL_API}/v2/checkout/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        intent: "CAPTURE",
        purchase_units: [
          {
            amount: {
              currency_code: "EUR",
              value: amount.toFixed(2),
            },
          },
        ],
      }),
    });

    const order = await orderRes.json();

    // 🔥 DEBUG IMPORTANT
    console.log("PayPal order response:", order);

    // ✅ CHECK IMPORTANT
    if (!order.id) {
      console.error("PayPal order error:", order);
      return NextResponse.json(
        { error: "Failed to create order", details: order },
        { status: 500 }
      );
    }

    return NextResponse.json({ id: order.id });

  } catch (err) {
    console.error("Create order server error:", err);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
