import type { Metadata } from "next";
import "./globals.css";
import ClientProviders from "./providers";

export const metadata: Metadata = {
  title: "Teacher-Student Management System",
  description: "Manage teachers, students, and classes",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen">
        <ClientProviders>{children}</ClientProviders>
      </body>
    </html>
  );
}
