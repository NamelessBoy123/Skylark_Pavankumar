import React, { useEffect, useState } from "react";

export default function AssignmentList() {
  const [assigns, setAssigns] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const res = await fetch("/api/assignments");
      const data = await res.json();
      setAssigns(data || []);
    } catch { setError("Failed to load assignments"); }
  }

  async function urgentReassign(project_id: string) {
    try {
      const res = await fetch("/api/urgent-reassign", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ project_id })
      });
      const data = await res.json();
      alert(data.message || "Reassignment result: " + JSON.stringify(data));
      load();
    } catch { setError("Urgent reassign failed"); }
  }

  return (
    <div className="list">
      <h2>Assignments</h2>
      {error && <div className="error">{error}</div>}
      <table>
        <thead><tr><th>Project</th><th>Pilot</th><th>Drone</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          {assigns.map((a, i) => (
            <tr key={i}>
              <td>{a.project_id}</td>
              <td>{a.pilot}</td>
              <td>{a.drone}</td>
              <td>{a.status}</td>
              <td><button onClick={() => urgentReassign(a.project_id)}>Urgent Reassign</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
