import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import PilotList from "./components/PilotList";
import DroneList from "./components/DroneList";
import AssignmentList from "./components/AssignmentList";
import Chat from "./components/Chat";
import "./styles.css";

export default function App() {
  const [view, setView] = useState<"dashboard" | "pilots" | "drones" | "assignments">("dashboard");

  return (
    <div className="app-root">
      <header className="topbar">
        <h1>Skylark — Drone Operations Coordinator</h1>
      </header>

      <div className="container">
        <nav className="sidebar">
          <button className={view === "dashboard" ? "active" : ""} onClick={() => setView("dashboard")}>Overview</button>
          <button className={view === "pilots" ? "active" : ""} onClick={() => setView("pilots")}>Pilots</button>
          <button className={view === "drones" ? "active" : ""} onClick={() => setView("drones")}>Drones</button>
          <button className={view === "assignments" ? "active" : ""} onClick={() => setView("assignments")}>Assignments</button>
        </nav>

        <main className="main">
          {view === "dashboard" && <Dashboard />}
          {view === "pilots" && <PilotList />}
          {view === "drones" && <DroneList />}
          {view === "assignments" && <AssignmentList />}
        </main>

        <aside className="chat-panel">
          <Chat />
        </aside>
      </div>

      <footer className="footer">© Skylark Drones — Coordinator UI</footer>
    </div>
  );
}
