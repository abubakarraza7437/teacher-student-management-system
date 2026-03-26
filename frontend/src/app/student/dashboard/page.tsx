"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/lib/auth";
import { getStudentDashboard, StudentDashboard } from "@/lib/api";

export default function StudentDashboardPage() {
  return (
    <ProtectedRoute allowedRoles={["student"]}>
      <DashboardContent />
    </ProtectedRoute>
  );
}

function DashboardContent() {
  const { token } = useAuth();
  const [data, setData] = useState<StudentDashboard | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    getStudentDashboard(token)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg">
        {error}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow p-6">
        <h1 className="text-2xl font-bold mb-1">
          Welcome, {data.user.name} 👋
        </h1>
        <p className="text-gray-500">{data.user.email}</p>
      </div>

      {/* Profile Card */}
      <div className="bg-white rounded-2xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Profile</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-indigo-50 rounded-xl p-4 text-center">
            <p className="text-sm text-gray-500">Dues</p>
            <p className="text-2xl font-bold text-indigo-700">
              {data.profile.dues ?? "—"}
            </p>
          </div>
          <div className="bg-amber-50 rounded-xl p-4 text-center">
            <p className="text-sm text-gray-500">Pending Dues</p>
            <p className="text-2xl font-bold text-amber-700">
              {data.profile.pending_dues ?? "—"}
            </p>
          </div>
          <div className="bg-green-50 rounded-xl p-4 text-center">
            <p className="text-sm text-gray-500">Status</p>
            <p className="text-2xl font-bold text-green-700">
              {data.profile.is_active ? "Active" : "Inactive"}
            </p>
          </div>
        </div>
      </div>

      {/* Classes */}
      <div className="bg-white rounded-2xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">
          My Classes ({data.classes.length})
        </h2>

        {data.classes.length === 0 ? (
          <p className="text-gray-400 text-center py-8">
            You are not enrolled in any classes yet.
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.classes.map((cls) => (
              <div
                key={cls.id}
                className="border border-gray-200 rounded-xl p-5 hover:shadow-md transition"
              >
                <h3 className="font-semibold text-lg">{cls.name}</h3>
                <p className="text-gray-500 text-sm mb-3">{cls.subject}</p>
                <div className="border-t pt-3">
                  <p className="text-xs text-gray-400 uppercase tracking-wide mb-1">
                    Teacher
                  </p>
                  <p className="font-medium">{cls.teacher.name ?? "—"}</p>
                  <p className="text-sm text-gray-500">
                    {cls.teacher.email ?? "—"}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
