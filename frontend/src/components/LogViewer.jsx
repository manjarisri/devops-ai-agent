import React from "react";
function LogViewer({ logs }) {
  if (!logs || logs.length === 0) {
    return (
      <div className="panel">
        <h2>Application Logs</h2>
        <p>No logs available.</p>
      </div>
    );
  }

  return (
    <div className="panel">

      <h2>📋 Application Logs</h2>

      {logs.map((item, index) => (
        <div key={index}>

          <h3>{item.pod}</h3>

          <pre className="logs">
            {item.raw_logs}
          </pre>

          <div>
            <strong>Detected signals:</strong>

            {item.analysis?.signals?.map(
              (signal) => (
                <span
                  className="tag"
                  key={signal}
                >
                  {signal}
                </span>
              )
            )}
          </div>

        </div>
      ))}

    </div>
  );
}

export default LogViewer;