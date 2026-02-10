import React, { useState } from "react";

type Msg = { role: "system" | "user" | "ai"; content: string };

export default function Chat() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "system", content: "Ask me about pilots, drones, assignments, or urgent reassignments." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim()) return;
    const userMsg = { role: "user" as const, content: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("/api/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.content, history: messages })
      });
      const data = await res.json();
      setMessages((m) => [...m, userMsg, { role: "ai", content: data.reply || "No response" }]);
    } catch (e) {
      setMessages((m) => [...m, userMsg, { role: "ai", content: "Error contacting backend." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat">
      <div className="chat-header">Coordinator Assistant</div>
      <div className="chat-body">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>
            <span className="role">{m.role}:</span> <span>{m.content}</span>
          </div>
        ))}
        {loading && <div className="chat-msg ai">AI is typing...</div>}
      </div>
      <div className="chat-input">
        <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === "Enter" && send()} placeholder="Ask the coordinator..." />
        <button onClick={send} disabled={loading}>Send</button>
      </div>
    </div>
  );
}
