import React, { useEffect, useState } from "react";

export default function Dashboard() {
  const [pilotCount, setPilotCount] = useState(0);
  const [droneCount, setDroneCount] = useState(0);
  const [assignCount, setAssignCount] = useState(0);
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [pRes, dRes, aRes, cRes] = await Promise.all([
          fetch("/api/pilots"),
          fetch("/api/drones"),
          fetch("/api/assignments"),
          fetch("/api/conflicts"),
        ]);
        const [pilots, drones, assigns, conf] = await Promise.all([pRes.json(), dRes.json(), aRes.json(), cRes.json()]);
        setPilotCount(pilots.length || 0);
        setDroneCount(drones.length || 0);
        setAssignCount(assigns.length || 0);
        setConflicts(conf.conflicts || []);
      } catch (e:any) {
        setError("Failed to load dashboard");
      }
    }
    load();
  }, []);

  return (
    <div className="dashboard">
      <h2>Overview</h2>
      {error && <div className="error">{error}</div>}
      <div className="cards">
        <div className="card"><div className="num">{pilotCount}</div><div>Pilots</div></div>
        <div className="card"><div className="num">{droneCount}</div><div>Drones</div></div>
        <div className="card"><div className="num">{assignCount}</div><div>Assignments</div></div>
      </div>

      <section>
        <h3>Active Conflicts</h3>
        {conflicts.length === 0 ? <div className="muted">No conflicts detected</div> :
          <ul>
            {conflicts.map((c, i) => <li key={i}>{c.type} — {c.pilot || c.drone} — {JSON.stringify(c.projects || c.details)}</li>)}
          </ul>}
      </section>
    </div>
  );
}
