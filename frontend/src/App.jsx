import React, { useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";
import IncidentPanel from "./components/IncidentPanel";
import StatusCard from "./components/StatusCard";


function Dashboard() {
  const [pods, setPods] = useState("Loading...");

  useEffect(() => {
    const loadPods = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/api/chat",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              message: "Show me my Kubernetes pods",
            }),
          }
        );

        const data = await response.json();

        /*
         * Backend may return Kubernetes data
         * in different formats depending on
         * the tool implementation.
         */
        if (Array.isArray(data.response)) {
          const running = data.response.filter(
            (pod) =>
              pod.phase === "Running" ||
              pod.status === "Running"
          ).length;

          setPods(`${running} Running`);
        } else {
          setPods("Available");
        }
      } catch (error) {
        console.error(
          "Failed to load pods:",
          error
        );

        setPods("Unavailable");
      }
    };

    loadPods();
  }, []);


  return (
    <div>
      <div className="page-header">
        <div>
          <h1>DevOps AI Dashboard</h1>

          <p>
            AI-powered DevOps investigation
            and operational intelligence
          </p>
        </div>

        <div className="online">
          ● Local Environment
        </div>
      </div>


      <div className="cards">

        <StatusCard
          title="Kubernetes"
          value="Healthy"
          subtitle="Minikube"
        />

        <StatusCard
          title="Pods"
          value={pods}
          subtitle="Current cluster"
        />

        <StatusCard
          title="Demo Incident"
          value="HIGH"
          subtitle="demo-app"
        />

        <StatusCard
          title="AI Provider"
          value="LOCAL"
          subtitle="Offline capable"
        />

      </div>


      <IncidentPanel />

    </div>
  );
}


function App() {
  const [active, setActive] = useState(
    "dashboard"
  );


  return (
    <div className="app">

      <Sidebar
        active={active}
        setActive={setActive}
      />


      <main className="main">

        {/* ============================= */}
        {/* Dashboard */}
        {/* ============================= */}

        {active === "dashboard" && (
          <Dashboard />
        )}


        {/* ============================= */}
        {/* Incident Investigation */}
        {/* ============================= */}

        {active === "incident" && (
          <IncidentPanel />
        )}


        {/* ============================= */}
        {/* Kubernetes Assistant */}
        {/* ============================= */}

        {active === "kubernetes" && (
          <Chat
            mode="kubernetes"
          />
        )}


        {/* ============================= */}
        {/* Deployment Review */}
        {/* ============================= */}

        {active === "deployment" && (
          <Chat
            mode="deployment"
          />
        )}


        {/* ============================= */}
        {/* Infrastructure as Code Review */}
        {/* ============================= */}

        {active === "iac" && (
          <Chat
            mode="iac"
          />
        )}

      </main>

    </div>
  );
}


export default App;