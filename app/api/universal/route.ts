import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(req: NextRequest) {
  const target = req.nextUrl.searchParams.get("target");
  if (!target) return NextResponse.json({ error: "No target specified" }, { status: 400 });
  const url = `${BACKEND_URL}/${target}`;
  const res = await fetch(url, { method: "GET" });
  const data = await res.json();
  return NextResponse.json(data);
}

export async function POST(req: NextRequest) {
  const target = req.nextUrl.searchParams.get("target");
  if (!target) return NextResponse.json({ error: "No target specified" }, { status: 400 });
  const url = `${BACKEND_URL}/${target}`;
  const body = await req.text();
  const res = await fetch(url, { method: "POST", body, headers: { "Content-Type": "application/json" } });
  const data = await res.json();
  return NextResponse.json(data);
}
