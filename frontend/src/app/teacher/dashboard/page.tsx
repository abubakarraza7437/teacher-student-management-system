"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/lib/auth";
import { getTeacherDashboard, TeacherDashboard } from "@/lib/api";

export default function TeacherDashboardPage() {
  return (
    <ProtectedRoute allowedRoles={["teacher"]}>
      <DashboardContent />
    </ProtectedRoute>
  );
}

function DashboardContent() {
  const { token } = useAuth();
  const [data, setData] = useState<TeacherDashboard | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    getTeacherDashboard(token)
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

  const totalStudents = data.classes.reduce((sum, c) => sum + c.students.length, 0);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow p-6">
        <h1 className="text-2xl font-bold mb-1">
          Welcome, {data.user.name} 🎓
        </h1>
        <p className="text-gray-500">{data.user.email}</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl shadow p-6 text-center">
          <p className="text-sm text-gray-500">Classes</p>
          <p className="text-3xl font-bold text-indigo-700">{data.classes.length}</p>
        </div>
        <div className="bg-white rounded-2xl shadow p-6 text-center">
          <p className="text-sm text-gray-500">Total Students</p>
          <p className="text-3xl font-bold text-green-700">{totalStudents}</p>
        </div>
        <div className="bg-white rounded-2xl shadow p-6 text-center">
          <p className="text-sm text-gray-500">Salary</p>
          <p className="text-3xl font-bold text-amber-700">
            {data.profile.salary != null ? `$${data.profile.salary}` : "—"}
          </p>
        </div>
      </div>

      {/* Classes */}
      <div className="bg-white rounded-2xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">
          My Classes ({data.classes.length})
        </h2>

        {data.classes.length === 0 ? (
          <p className="text-gray-400 text-center py-8">
            You haven&apos;t created any classes yet.
          </p>
        ) : (
          <div className="space-y-4">
            {data.classes.map((cls) => (
              <div
                key={cls.id}
                className="border border-gray-200 rounded-xl p-5 hover:shadow-md transition"
              >
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-lg">{cls.name}</h3>
                    <p className="text-gray-500 text-sm">{cls.subject}</p>
                  </div>
                  <span className="bg-indigo-100 text-indigo-700 text-xs font-medium px-3 py-1 rounded-full">
                    {cls.students.length} student{cls.students.length !== 1 ? "s" : ""}
                  </span>
                </div>

                {cls.students.length > 0 && (
                  <div className="border-t pt-3">
                    <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">
                      Enrolled Students
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                      {cls.students.map((s) => (
                        <div
                          key={s.id}
                          className="bg-gray-50 rounded-lg px-3 py-2 text-sm"
                        >
                          <p className="font-medium">{s.name}</p>
                          <p className="text-gray-500 text-xs">{s.email}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
