import React, { useEffect, useState } from "react";

function IncidentPanel() {
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(false);

  const investigate = async () => {
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/incidents/demo-app"
      );

      const data = await response.json();

      setIncident(data);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  useEffect(() => {
    investigate();
  }, []);

  if (loading) {
    return (
      <div className="panel">
        <h2>Incident Investigation</h2>
        <p>Investigating demo-app...</p>
      </div>
    );
  }

  if (!incident) {
    return null;
  }

  const analysis = incident.analysis;
  const evidence = incident.evidence;

  return (
    <div className="panel">

      <div className="panel-header">
        <div>
          <h2>🚨 Incident Investigation</h2>
          <p>Application: demo-app</p>
        </div>

        <button onClick={investigate}>
          Investigate Again
        </button>
      </div>

      <div className="status-row">

        <div className="status-box">
          <span>Status</span>
          <strong>{analysis.status}</strong>
        </div>

        <div className="status-box">
          <span>Severity</span>
          <strong>{analysis.severity}</strong>
        </div>

        <div className="status-box">
          <span>Confidence</span>
          <strong>
            {Math.round(
              analysis.confidence * 100
            )}%
          </strong>
        </div>

      </div>

      <section>
        <h3>Root Cause</h3>

        <div className="root-cause">
          {analysis.root_cause}
        </div>
      </section>

      <section>
        <h3>Findings</h3>

        <ul>
          {analysis.findings?.map(
            (finding, index) => (
              <li key={index}>
                {finding}
              </li>
            )
          )}
        </ul>
      </section>

      <section>
        <h3>Recommendations</h3>

        <ol>
          {analysis.recommendations?.map(
            (recommendation, index) => (
              <li key={index}>
                {recommendation}
              </li>
            )
          )}
        </ol>
      </section>

      <section>
        <h3>Kubernetes Evidence</h3>

        <pre>
          {JSON.stringify(
            evidence.events,
            null,
            2
          )}
        </pre>
      </section>

    </div>
  );
}

export default IncidentPanel;