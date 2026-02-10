import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([{ role: "system", content: "How can I help coordinate your drone operations today?" }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, history: newMessages }),
      });
      const data = await res.json();
      setMessages([...newMessages, { role: "ai", content: data.reply || "No response." }]);
    } catch (err) {
      setMessages([...newMessages, { role: "ai", content: "Sorry, there was an error connecting to the backend." }]);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto" }}>
      <h2>Drone Operations Coordinator AI</h2>
      <div style={{ minHeight: 200, border: "1px solid #ccc", padding: 16, marginBottom: 16 }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ color: msg.role === "user" ? "#333" : msg.role === "ai" ? "#0078d4" : "#888" }}>
            <b>{msg.role}:</b> {msg.content}
          </div>
        ))}
        {loading && <div style={{ color: "#aaa" }}>AI is typing...</div>}
      </div>
      <input
        style={{ width: "80%" }}
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === "Enter" && sendMessage()}
        placeholder="Type your request..."
        disabled={loading}
      />
      <button onClick={sendMessage} disabled={loading}>Send</button>
    </div>
  );
}

export default App;
