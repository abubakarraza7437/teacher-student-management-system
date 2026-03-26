"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const { user, logout, loading } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <nav className="bg-indigo-700 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold tracking-tight">
            📚 TSMS
          </Link>

          <div className="flex items-center gap-4">
            {loading ? null : user ? (
              <>
                {user.role === "teacher" && (
                  <>
                    <Link href="/teacher/dashboard" className="hover:text-indigo-200 transition">
                      Dashboard
                    </Link>
                    <Link href="/teacher/classes" className="hover:text-indigo-200 transition">
                      Classes
                    </Link>
                  </>
                )}
                {user.role === "student" && (
                  <Link href="/student/dashboard" className="hover:text-indigo-200 transition">
                    Dashboard
                  </Link>
                )}
                {user.role === "admin" && (
                  <Link href="/admin/users" className="hover:text-indigo-200 transition">
                    Users
                  </Link>
                )}
                <span className="text-indigo-200 text-sm">
                  {user.name} ({user.role})
                </span>
                <button
                  onClick={handleLogout}
                  className="bg-indigo-500 hover:bg-indigo-400 px-3 py-1 rounded text-sm transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="hover:text-indigo-200 transition">
                  Login
                </Link>
                <Link
                  href="/register"
                  className="bg-white text-indigo-700 px-3 py-1 rounded font-medium hover:bg-indigo-50 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
