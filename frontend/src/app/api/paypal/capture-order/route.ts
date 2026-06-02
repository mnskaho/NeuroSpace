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
  return data.access_token;
}

export async function POST(req: Request) {
  const { orderID } = await req.json();

  const accessToken = await getAccessToken();

  const captureRes = await fetch(
    `${PAYPAL_API}/v2/checkout/orders/${orderID}/capture`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  const data = await captureRes.json();

  if (data.status !== "COMPLETED") {
    return NextResponse.json({ error: "Payment not completed" }, { status: 400 });
  }

  return NextResponse.json(data);
}