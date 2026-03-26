"use client";

import { AuthProvider } from "@/lib/auth";
import Navbar from "@/components/Navbar";

export default function ClientProviders({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">{children}</main>
    </AuthProvider>
  );
}
