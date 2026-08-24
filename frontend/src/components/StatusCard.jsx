import React from "react";

function StatusCard({
  title,
  value,
  subtitle,
}) {
  return (
    <div className="status-card">

      <div className="status-title">
        {title}
      </div>

      <div className="status-value">
        {value}
      </div>

      {subtitle && (
        <div className="status-subtitle">
          {subtitle}
        </div>
      )}

    </div>
  );
}

export default StatusCard;