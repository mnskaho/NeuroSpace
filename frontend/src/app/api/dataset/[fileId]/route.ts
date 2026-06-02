import { NextResponse } from 'next/server';

export const runtime = 'nodejs';

const BACKEND_BASE_URL = (
  process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:7000/api'
).replace(/\/+$/, '');

export async function GET(_req: Request, { params }: { params: Promise<{ fileId: string }> }) {
  const { fileId } = await params;
  const response = await fetch(`${BACKEND_BASE_URL}/dataset/${fileId}`);

  if (!response.ok) {
    return NextResponse.json({ error: 'Dataset not found' }, { status: response.status });
  }

  const body = await response.arrayBuffer();
  return new NextResponse(body, {
    headers: {
      'Content-Type': response.headers.get('content-type') || 'text/csv',
      'Content-Disposition':
        response.headers.get('content-disposition') || `attachment; filename="${fileId}.csv"`,
    },
  });
}
