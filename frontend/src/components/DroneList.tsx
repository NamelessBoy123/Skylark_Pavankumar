import React, { useEffect, useState } from "react";

export default function DroneList() {
  const [drones, setDrones] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const res = await fetch("/api/drones");
      const data = await res.json();
      setDrones(data || []);
    } catch { setError("Failed to load drones"); }
  }

  async function updateStatus(serial: string, status: string) {
    try {
      await fetch("/api/drone/status", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ serial, status })
      });
      load();
    } catch { setError("Failed to update"); }
  }

  return (
    <div className="list">
      <h2>Drone Fleet</h2>
      {error && <div className="error">{error}</div>}
      <table>
        <thead><tr><th>Model</th><th>Serial</th><th>Capabilities</th><th>Location</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          {drones.map((d, i) => (
            <tr key={i}>
              <td>{d.model}</td>
              <td>{d.serial_number}</td>
              <td>{d.capabilities}</td>
              <td>{d.current_location}</td>
              <td>{d.status}</td>
              <td>
                <select defaultValue={d.status} onChange={e => updateStatus(d.serial_number, e.target.value)}>
                  <option>Available</option>
                  <option>Maintenance</option>
                  <option>Deployed</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
