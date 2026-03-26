"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;
    if (!user) {
      router.replace("/login");
      return;
    }
    if (user.role === "teacher") router.replace("/teacher/dashboard");
    else if (user.role === "student") router.replace("/student/dashboard");
    else if (user.role === "admin") router.replace("/admin/users");
    else router.replace("/login");
  }, [user, loading, router]);

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
    </div>
  );
}
