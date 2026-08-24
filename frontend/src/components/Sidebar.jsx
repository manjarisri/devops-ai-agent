import React from "react";

function Sidebar({ active, setActive }) {

  const items = [
    ["dashboard", "📊 Dashboard"],
    ["incident", "🚨 Incident Investigation"],
    ["kubernetes", "☸ Kubernetes"],
    ["deployment", "🚀 Deployment Review"],
    ["iac", "🏗 IaC Review"],
  ];

  return (
    <aside className="sidebar">

      <h1>DevOps AI</h1>

      <p className="subtitle">
        Local AI Assistant
      </p>

      <nav>

        {items.map(([id, label]) => (

          <button
            key={id}
            className={
              active === id
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => setActive(id)}
          >
            {label}
          </button>

        ))}

      </nav>

      <div className="provider">

        <span>AI Provider</span>

        <strong>
          Local Demo Engine
        </strong>

        <small>
          Azure OpenAI ready
        </small>

      </div>

    </aside>
  );
}

export default Sidebar;