import type { Metadata } from "next";
import { Toaster } from "sonner";
import "./globals.css";

export const metadata: Metadata = {
  title: "AETHERIS SOC | AI-Based Network Threat Detection Platform",
  description: "Real-time AI-driven cybersecurity monitoring platform powered by XGBoost, Isolation Forest, and event streaming",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#030712] text-slate-100 min-h-screen antialiased selection:bg-cyan-500 selection:text-black">
        {children}
        <Toaster
          theme="dark"
          position="bottom-right"
          richColors
          toastOptions={{
            style: {
              background: "#090d16",
              border: "1px solid #1e293b",
              color: "#f8fafc",
              fontFamily: "monospace",
              fontSize: "12px",
            },
          }}
        />
      </body>
    </html>
  );
}
