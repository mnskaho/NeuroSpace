import { NextResponse } from 'next/server';

export const runtime = 'nodejs';

const BACKEND_BASE_URL = (
  process.env.NEXT_PUBLIC_BACKEND_URL ||
  process.env.BACKEND_URL ||
  ''
).replace(/\/+$/, '');

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ fileId: string }> }
) {
  try {
    const { fileId } = await params;

    if (!BACKEND_BASE_URL) {
      return NextResponse.json(
        { error: 'NEXT_PUBLIC_BACKEND_URL is not configured on Vercel' },
        { status: 500 }
      );
    }

    const backendResponse = await fetch(
      `${BACKEND_BASE_URL}/report/${fileId}/pdf`,
      {
        method: 'GET',
        cache: 'no-store',
      }
    );

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text().catch(() => '');

      return NextResponse.json(
        {
          error: 'Failed to fetch PDF from backend',
          backendStatus: backendResponse.status,
          details: errorText,
        },
        { status: backendResponse.status }
      );
    }

    const pdfBuffer = await backendResponse.arrayBuffer();

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${fileId}_report.pdf"`,
      },
    });
  } catch (error) {
    console.error('PDF proxy error:', error);

    return NextResponse.json(
      { error: 'Internal PDF proxy error' },
      { status: 500 }
    );
  }
}