import React, { useState } from "react";


const API_URL = "http://localhost:8000";


function Chat({ mode = "kubernetes" }) {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);


  const config = {
    kubernetes: {
      title: "Kubernetes Assistant",

      description:
        "Inspect your Minikube cluster, pods, deployments and Kubernetes health.",

      placeholder:
        "Example: Show me my Kubernetes pods",

      button: "Ask Kubernetes",

      defaultMessage:
        "Show me my Kubernetes pods",
    },


    deployment: {
      title: "Deployment Review",

      description:
        "Review Kubernetes deployment configuration and receive DevOps recommendations.",

      placeholder:
        "Paste a Kubernetes Deployment YAML here",

      button: "Review Deployment",
    },


    iac: {
      title: "IaC Review",

      description:
        "Review Infrastructure as Code for security and configuration issues.",

      placeholder:
        "Paste Terraform or Infrastructure as Code here",

      button: "Review IaC",
    },
  };


  const current = config[mode];


  const handleSubmit = async () => {

    const input = message.trim();


    if (!input && mode !== "kubernetes") {
      return;
    }


    setLoading(true);
    setResponse("");


    try {

      let url;
      let body;


      // ==========================================
      // Kubernetes Chat
      // ==========================================

      if (mode === "kubernetes") {

        url = `${API_URL}/api/chat`;

        body = {
          message:
            input || current.defaultMessage,
        };

      }


      // ==========================================
      // Deployment Review
      // Backend route:
      // POST /api/reviews/deployment
      // ==========================================

      else if (mode === "deployment") {

        url = `${API_URL}/api/reviews/deployment`;

        body = {
          content: input,
        };

      }


      // ==========================================
      // IaC Review
      // Backend route:
      // POST /api/reviews/iac
      // ==========================================

      else {

        url = `${API_URL}/api/reviews/iac`;

        body = {
          content: input,
          iac_type: "terraform",
        };

      }


      const result = await fetch(
        url,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(body),
        }
      );


      const data = await result.json();


      // ==========================================
      // Handle API errors
      // ==========================================

      if (!result.ok) {

        setResponse(
          JSON.stringify(
            data,
            null,
            2
          )
        );

        return;
      }


      // ==========================================
      // Format Kubernetes response
      // ==========================================

      if (mode === "kubernetes") {

        if (Array.isArray(data.response)) {

          const formatted = data.response
            .map((item) => {

              const name =
                item.name || "Unknown";

              const namespace =
                item.namespace || "default";

              const phase =
                item.phase ||
                item.status ||
                "Unknown";

              return (
                `Pod: ${name}\n` +
                `Namespace: ${namespace}\n` +
                `Status: ${phase}`
              );

            })
            .join("\n\n");

          setResponse(formatted);

        }

        else if (
          typeof data.response === "string"
        ) {

          setResponse(data.response);

        }

        else {

          setResponse(
            JSON.stringify(
              data.response || data,
              null,
              2
            )
          );

        }

      }


      // ==========================================
      // Format Deployment / IaC recommendations
      // ==========================================

      else if (data.recommendations) {

        if (data.recommendations.length === 0) {

          setResponse(
            "No major issues were detected in the provided configuration."
          );

        } else {

          const formatted =
            data.recommendations
              .map(
                (item, index) =>
                  `${index + 1}. ${item}`
              )
              .join("\n\n");

          setResponse(formatted);

        }

      }


      // ==========================================
      // Fallback response
      // ==========================================

      else {

        setResponse(
          JSON.stringify(
            data,
            null,
            2
          )
        );

      }

    } catch (error) {

      console.error(
        "DevOps AI request failed:",
        error
      );

      setResponse(
        "Unable to contact the DevOps AI backend. " +
        "Please make sure the FastAPI backend is running on port 8000."
      );

    } finally {

      setLoading(false);

    }

  };


  // ==========================================
  // Load Demo Examples
  // ==========================================

  const loadExample = () => {


    // Kubernetes example
    if (mode === "kubernetes") {

      setMessage(
        "Show me my Kubernetes pods"
      );

    }


    // Deployment example
    else if (mode === "deployment") {

      setMessage(`apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-app

  template:
    metadata:
      labels:
        app: demo-app

    spec:
      containers:
        - name: demo-app
          image: demo-app:latest`);

    }


    // IaC example
    else if (mode === "iac") {

      setMessage(`resource "aws_security_group" "demo" {
  name = "demo-security-group"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
}

resource "aws_db_instance" "demo" {
  identifier = "demo-database"

  password = "admin123"
}`);

    }

  };


  return (

    <div className="chat-page">


      {/* ===================================== */}
      {/* Page Header */}
      {/* ===================================== */}

      <div className="feature-header">

        <h1>
          {current.title}
        </h1>

        <p>
          {current.description}
        </p>

      </div>


      {/* ===================================== */}
      {/* Demo Example Button */}
      {/* ===================================== */}

      <div className="chat-toolbar">

        <button
          className="example-button"
          onClick={loadExample}
        >
          Load Demo Example
        </button>

      </div>


      {/* ===================================== */}
      {/* Response Area */}
      {/* ===================================== */}

      <div className="chat-response">


        {!response && !loading && (

          <div className="empty-state">

            <h3>
              Ready for analysis
            </h3>

            <p>

              {mode === "kubernetes"
                ? "Ask a question about your local Kubernetes cluster."
                : "Load the demo example or paste your own configuration."}

            </p>

          </div>

        )}


        {loading && (

          <div className="loading">

            DevOps AI is analyzing...

          </div>

        )}


        {response && (

          <pre className="response-output">

            {response}

          </pre>

        )}


      </div>


      {/* ===================================== */}
      {/* Input Area */}
      {/* ===================================== */}

      <div className="chat-input-area">

        <textarea
          value={message}

          onChange={(event) =>
            setMessage(event.target.value)
          }

          placeholder={
            current.placeholder
          }

          rows="10"
        />


        <button
          className="send-button"

          onClick={handleSubmit}

          disabled={loading}
        >

          {loading
            ? "Analyzing..."
            : current.button}

        </button>

      </div>


    </div>

  );

}


export default Chat;