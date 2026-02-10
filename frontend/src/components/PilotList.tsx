import React, { useEffect, useState } from "react";

export default function PilotList() {
  const [pilots, setPilots] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const res = await fetch("/api/pilots");
      const data = await res.json();
      setPilots(data || []);
    } catch { setError("Failed to load pilots"); }
  }

  async function updateStatus(name: string, status: string) {
    try {
      await fetch("/api/pilot/status", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ name, status })
      });
      load();
    } catch { setError("Failed to update"); }
  }

  return (
    <div className="list">
      <h2>Pilot Roster</h2>
      {error && <div className="error">{error}</div>}
      <table>
        <thead><tr><th>Name</th><th>Skills</th><th>Location</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          {pilots.map((p, i) => (
            <tr key={i}>
              <td>{p.name}</td>
              <td>{p.certifications || p.skills}</td>
              <td>{p.current_location || p.location}</td>
              <td>{p.status}</td>
              <td>
                <select defaultValue={p.status} onChange={e => updateStatus(p.name, e.target.value)}>
                  <option>Available</option>
                  <option>On Leave</option>
                  <option>Unavailable</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
