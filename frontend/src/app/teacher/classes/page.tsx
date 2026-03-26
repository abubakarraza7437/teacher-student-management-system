"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/lib/auth";
import { createClass, getClasses, addStudentsToClass } from "@/lib/api";

interface ClassItem {
  id: string;
  name: string;
  subject: string;
  teacher_id: string;
  created_at: string;
  updated_at: string;
}

export default function TeacherClassesPage() {
  return (
    <ProtectedRoute allowedRoles={["teacher"]}>
      <ClassesContent />
    </ProtectedRoute>
  );
}

function ClassesContent() {
  const { token, user } = useAuth();
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Create class form
  const [showCreate, setShowCreate] = useState(false);
  const [className, setClassName] = useState("");
  const [subject, setSubject] = useState("");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState("");

  // Add students form
  const [addingTo, setAddingTo] = useState<string | null>(null);
  const [emails, setEmails] = useState("");
  const [addResult, setAddResult] = useState<{ added: string[]; not_found?: string[] } | null>(null);
  const [addError, setAddError] = useState("");
  const [addSubmitting, setAddSubmitting] = useState(false);

  const fetchClasses = () => {
    if (!token) return;
    setLoading(true);
    getClasses(token)
      .then(setClasses)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchClasses();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !user) return;
    setCreating(true);
    setCreateError("");
    try {
      await createClass(token, { name: className, subject, email: user.email });
      setClassName("");
      setSubject("");
      setShowCreate(false);
      fetchClasses();
    } catch (err: unknown) {
      setCreateError(err instanceof Error ? err.message : "Failed to create class");
    } finally {
      setCreating(false);
    }
  };

  const handleAddStudents = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !addingTo) return;
    setAddSubmitting(true);
    setAddError("");
    setAddResult(null);
    try {
      const emailList = emails
        .split(/[,\n]/)
        .map((s) => s.trim())
        .filter(Boolean);
      const result = await addStudentsToClass(token, {
        class_name: addingTo,
        emails: emailList,
      });
      setAddResult(result);
      setEmails("");
    } catch (err: unknown) {
      setAddError(err instanceof Error ? err.message : "Failed to add students");
    } finally {
      setAddSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Class Management</h1>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition"
        >
          {showCreate ? "Cancel" : "+ New Class"}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Create Class Form */}
      {showCreate && (
        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Create New Class</h2>
          {createError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">
              {createError}
            </div>
          )}
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Class Name</label>
              <input
                type="text"
                required
                value={className}
                onChange={(e) => setClassName(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="e.g. Mathematics 101"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
              <input
                type="text"
                required
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="e.g. Mathematics"
              />
            </div>
            <button
              type="submit"
              disabled={creating}
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 transition disabled:opacity-50"
            >
              {creating ? "Creating…" : "Create Class"}
            </button>
          </form>
        </div>
      )}

      {/* Classes List */}
      {classes.length === 0 ? (
        <div className="bg-white rounded-2xl shadow p-8 text-center text-gray-400">
          No classes yet. Create your first class!
        </div>
      ) : (
        <div className="space-y-4">
          {classes.map((cls) => (
            <div key={cls.id} className="bg-white rounded-2xl shadow p-6">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-lg">{cls.name}</h3>
                  <p className="text-gray-500 text-sm">{cls.subject}</p>
                </div>
                <button
                  onClick={() => {
                    setAddingTo(addingTo === cls.name ? null : cls.name);
                    setAddResult(null);
                    setAddError("");
                    setEmails("");
                  }}
                  className="text-indigo-600 hover:text-indigo-800 text-sm font-medium transition"
                >
                  {addingTo === cls.name ? "Close" : "+ Add Students"}
                </button>
              </div>

              {/* Add Students Form */}
              {addingTo === cls.name && (
                <div className="border-t pt-4 mt-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">
                    Add Students to {cls.name}
                  </h4>
                  {addError && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg mb-3 text-sm">
                      {addError}
                    </div>
                  )}
                  {addResult && (
                    <div className="mb-3 space-y-1">
                      {addResult.added.length > 0 && (
                        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-2 rounded-lg text-sm">
                          Added: {addResult.added.join(", ")}
                        </div>
                      )}
                      {addResult.not_found && addResult.not_found.length > 0 && (
                        <div className="bg-amber-50 border border-amber-200 text-amber-700 px-4 py-2 rounded-lg text-sm">
                          Not found: {addResult.not_found.join(", ")}
                        </div>
                      )}
                    </div>
                  )}
                  <form onSubmit={handleAddStudents} className="flex gap-3">
                    <input
                      type="text"
                      value={emails}
                      onChange={(e) => setEmails(e.target.value)}
                      placeholder="student1@email.com, student2@email.com"
                      className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <button
                      type="submit"
                      disabled={addSubmitting}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition disabled:opacity-50"
                    >
                      {addSubmitting ? "Adding…" : "Add"}
                    </button>
                  </form>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
