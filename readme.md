# 🤖 DevOps AI Assistant

A hands-on DevOps AI demo that combines Kubernetes, incident investigation, deployment reviews, and Infrastructure as Code reviews into a single dashboard.

The project runs locally using:

- React + Vite
- FastAPI
- Minikube
- Docker Desktop
- Kubernetes
- A local AI provider

The application is designed so that the local AI provider can later be replaced with **Azure OpenAI** without changing the main application architecture.

---

# 📌 Features

The DevOps AI Assistant currently provides five main capabilities.

## 1. 📊 DevOps Dashboard

The dashboard provides a quick overview of the local DevOps environment.

It displays:

- Kubernetes cluster status
- Pod availability
- Demo incident severity
- AI provider status

The current demo runs against a local Minikube Kubernetes cluster.

---

## 2. 🚨 Incident Investigation

The application can investigate a simulated Kubernetes incident.

The demo application is intentionally configured with a broken dependency that causes the application to fail.

The investigation collects:

- Pod status
- Container status
- Restart count
- Application logs
- Kubernetes events
- Deployment availability

The collected evidence is analyzed to determine:

- Incident severity
- Findings
- Probable root cause
- Confidence level
- Recommended troubleshooting steps

### Example Incident

The demo application experiences:

```text
Database connectivity / DNS resolution failure
        ↓
Application exits during startup
        ↓
Container restarts repeatedly
        ↓
CrashLoopBackOff
        ↓
Deployment has 0 available replicas
```

The DevOps AI Assistant correlates this information and produces a root cause such as:

> The application is failing during startup because it cannot resolve or connect to its required database dependency. The database connectivity failure causes the container to exit repeatedly, resulting in CrashLoopBackOff.

---

## 3. ☸️ Kubernetes Assistant

Users can ask questions about the local Kubernetes cluster.

Example questions:

```text
Show me my Kubernetes pods
```

```text
Show me my Kubernetes deployments
```

```text
Show me my Kubernetes services
```

The backend maps the request to Kubernetes tools and retrieves information from the Minikube cluster.

Example flow:

```text
User Request
     ↓
React Dashboard
     ↓
FastAPI API
     ↓
DevOps Tool Selection
     ↓
Kubernetes API
     ↓
Response
```

---

## 4. 🚀 Deployment Review

The application can review Kubernetes Deployment YAML files and identify common configuration issues.

Example deployment:

```yaml
apiVersion: apps/v1
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
          image: demo-app:latest
```

The local AI provider can identify recommendations such as:

- Add CPU and memory requests and limits.
- Consider adding a liveness probe.
- Consider adding a readiness probe.
- Consider multiple replicas for high availability.

---

## 5. 🏗️ Infrastructure as Code Review

The application can review Infrastructure as Code for common security and configuration issues.

Example Terraform:

```hcl
resource "aws_security_group" "demo" {

  name = "demo-security-group"

  ingress {

    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
}


resource "aws_db_instance" "demo" {

  identifier = "demo-database"

  password = "admin123"

}
```

The system can identify issues such as:

- Hard-coded passwords or secrets.
- Unrestricted network access.
- Mutable image tags.

---

# 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                  React Dashboard
                           │
                           ▼
                    FastAPI Backend
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
       Kubernetes      Incident        Deployment /
          Tools        Analyzer         IaC Review
            │              │              │
            └──────────────┼──────────────┘
                           │
                           ▼
                      AI Provider
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          Local AI Provider      Azure OpenAI
            Current Demo            Future
```

---

# 📁 Project Structure

```text
devops-ai-agent/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── incidents.py
│   │   │   └── reviews.py
│   │   │
│   │   ├── agent/
│   │   │   └── agent.py
│   │   │
│   │   ├── ai/
│   │   │   ├── base.py
│   │   │   └── local_provider.py
│   │   │
│   │   ├── analysis/
│   │   │   └── incident_analyzer.py
│   │   │
│   │   └── tools/
│   │       ├── kubernetes.py
│   │       ├── docker.py
│   │       └── jenkins.py
│   │
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   │
│   │   ├── components/
│   │   │   ├── Chat.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatusCard.jsx
│   │   │   └── IncidentPanel.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   └── package.json
│
├── demo-app/
│   ├── deployment.yaml
│   └── service.yaml
│
├── k8s/
│   ├── namespace.yaml
│   ├── backend.yaml
│   ├── frontend.yaml
│   └── service.yaml
│
├── docker-compose.yml
│
├── .env.example
│
└── README.md
```

---

# 🛠️ Prerequisites

Install the following tools before running the project.

## Required

### Python

Install Python 3.10 or later.

Verify:

```bash
python --version
```

---

### Node.js

Install Node.js.

Verify:

```bash
node -v
npm -v
```

---

### Docker Desktop

Docker Desktop is required because Minikube uses the Docker driver.

Verify:

```bash
docker ps
```

An empty container list is fine. It means Docker is running but there are currently no containers.

---

### Minikube

Install Minikube.

Verify:

```bash
minikube version
```

---

### kubectl

Verify:

```bash
kubectl version --client
```

---

# 🚀 Getting Started

## Step 1: Clone the Repository

```bash
git clone <YOUR-REPOSITORY-URL>
```

Move into the project:

```bash
cd devops-ai-agent
```

---

# ☸️ Step 2: Start Minikube

Make sure Docker Desktop is running.

Start Minikube:

```bash
minikube start --driver=docker
```

Check cluster status:

```bash
minikube status
```

Expected:

```text
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

Check nodes:

```bash
kubectl get nodes
```

Expected:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...
```

---

# 🐳 Step 3: Deploy the Demo Application

The demo application is intentionally unhealthy.

Apply the Kubernetes configuration:

```bash
kubectl apply -f demo-app/deployment.yaml
```

Apply the service:

```bash
kubectl apply -f demo-app/service.yaml
```

Check the pods:

```bash
kubectl get pods
```

You should eventually see something similar to:

```text
demo-app-xxxxxxxxxx-xxxxx   0/1   CrashLoopBackOff
demo-app-xxxxxxxxxx-xxxxx   0/1   CrashLoopBackOff
```

This is intentional.

The broken application creates a realistic incident that the DevOps AI Assistant can investigate.

---

# 🐍 Step 4: Start the Backend

Open a terminal.

Move into the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend should start at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# ⚛️ Step 5: Start the Frontend

Open a second terminal.

Move to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React application:

```bash
npm run dev
```

The application should be available at:

```text
http://localhost:5173
```

Open it in your browser.

---

# 🧪 Testing the Backend

## Kubernetes Chat

Example PowerShell request:

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/api/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"message":"Show me my Kubernetes pods"}'
```

---

## Incident Investigation

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/api/incidents/demo-app" `
  -Method GET
```

To see the complete response:

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/api/incidents/demo-app" `
  -Method GET |
  ConvertTo-Json -Depth 10
```

The response includes:

- Kubernetes pods
- Container state
- Restart counts
- Logs
- Kubernetes events
- Deployment status
- Findings
- Root cause
- Recommendations
- Confidence

---

# 🎬 How to Run the Demo

Once Minikube, the backend, and the frontend are running, open:

```text
http://localhost:5173
```

Follow the demo in this order.

---

## 1. Dashboard

Show:

- Kubernetes status
- Pod status
- Demo incident severity
- AI provider status

### Suggested explanation

> This dashboard provides a centralized view of the local DevOps environment. The demo integrates Kubernetes operational data with an AI analysis layer.

---

## 2. Kubernetes Assistant

Open:

```text
Kubernetes
```

Click:

```text
Load Demo Example
```

Then click:

```text
Ask Kubernetes
```

Example questions:

```text
Show me my Kubernetes pods
```

```text
Show me my Kubernetes deployments
```

```text
Show me my Kubernetes services
```

### Suggested explanation

> The assistant interprets the request and connects it to the appropriate DevOps tooling. In this demo, it retrieves real information from the Minikube Kubernetes cluster.

---

## 3. Incident Investigation

Open:

```text
Incident Investigation
```

The application investigates the intentionally broken `demo-app`.

Show:

- CrashLoopBackOff
- Database or DNS connectivity failure
- Findings
- Root cause
- Confidence
- Recommendations

### Suggested explanation

> Instead of manually checking pods, logs, events, and deployments separately, the system automatically collects and correlates the evidence.

---

## 4. Deployment Review

Open:

```text
Deployment Review
```

Click:

```text
Load Demo Example
```

Then:

```text
Review Deployment
```

The system should recommend improvements related to:

- Resource limits
- Liveness probes
- Readiness probes
- High availability

### Suggested explanation

> This demonstrates a proactive use case where DevOps AI reviews a configuration before it reaches production.

---

## 5. IaC Review

Open:

```text
IaC Review
```

Click:

```text
Load Demo Example
```

Then:

```text
Review IaC
```

The example demonstrates detection of:

- Hard-coded credentials
- Unrestricted network access

### Suggested explanation

> The same AI-assisted approach can be applied earlier in the engineering lifecycle to identify potential infrastructure and security issues before deployment.

---

# 🧠 AI Provider Architecture

The project uses a provider abstraction.

Current provider:

```text
LocalAIProvider
```

The application uses the following interface:

```python
class AIProvider:

    def analyze_incident(
        self,
        evidence: dict,
    ) -> dict:
        pass


    def review_deployment(
        self,
        deployment: str,
    ) -> dict:
        pass


    def review_iac(
        self,
        content: str,
        iac_type: str,
    ) -> dict:
        pass
```

The current implementation uses local rule-based analysis.

```text
LocalAIProvider
```

This allows the demo to run without:

- Azure subscription
- OpenAI API key
- Internet access
- Cloud infrastructure

---

# ☁️ Future Azure OpenAI Integration

The project is designed to support Azure OpenAI.

A future provider can be implemented as:

```text
AzureOpenAIProvider
```

The architecture would become:

```text
AIProvider
    │
    ├── LocalAIProvider
    │
    └── AzureOpenAIProvider
```

The Azure provider would implement the same methods:

```python
analyze_incident()

review_deployment()

review_iac()
```

Only the provider selection layer needs to change.

The rest of the application can remain unchanged.

Example future configuration:

```env
AI_PROVIDER=azure

AZURE_OPENAI_ENDPOINT=<your-endpoint>

AZURE_OPENAI_API_KEY=<your-api-key>

AZURE_OPENAI_DEPLOYMENT=<your-model-deployment>
```

---

# 🔄 Complete Request Flow

## Kubernetes Query

```text
User
  ↓
React Frontend
  ↓
POST /api/chat
  ↓
FastAPI
  ↓
Kubernetes Tool
  ↓
Minikube Cluster
  ↓
Kubernetes Response
  ↓
Frontend
```

---

## Incident Investigation

```text
User
  ↓
Incident Investigation Dashboard
  ↓
GET /api/incidents/demo-app
  ↓
Collect Kubernetes Evidence
  │
  ├── Pods
  ├── Container State
  ├── Restart Count
  ├── Logs
  ├── Events
  └── Deployment Status
        ↓
Incident Analyzer
        ↓
AI Provider
        ↓
Root Cause
Findings
Recommendations
Confidence
```

---

## Deployment Review

```text
User YAML
    ↓
React Frontend
    ↓
POST /api/reviews/deployment
    ↓
Agent
    ↓
AI Provider
    ↓
Recommendations
```

---

## IaC Review

```text
Terraform / IaC
       ↓
React Frontend
       ↓
POST /api/reviews/iac
       ↓
Agent
       ↓
AI Provider
       ↓
Security / Configuration Recommendations
```

---

# 🔧 Troubleshooting

## Docker is not running

Check:

```bash
docker ps
```

Make sure Docker Desktop is running.

---

## Minikube is not starting

Check status:

```bash
minikube status
```

Delete and recreate the cluster if required:

```bash
minikube delete
```

Then:

```bash
minikube start --driver=docker
```

---

## Backend shows `ModuleNotFoundError: No module named 'app'`

Make sure you are inside the `backend` directory:

```bash
cd backend
```

Then run:

```bash
uvicorn app.main:app --reload
```

---

## Frontend shows a blank page

Check the browser developer console.

Also verify that:

```bash
npm run dev
```

is running successfully.

---

## `npm` is not recognized

Install Node.js and restart VS Code.

Verify:

```bash
node -v
npm -v
```

---

## API returns `404 Not Found`

Verify that the backend is running:

```text
http://localhost:8000/health
```

Also verify the correct API routes:

```text
POST /api/chat

GET /api/incidents/demo-app

POST /api/reviews/deployment

POST /api/reviews/iac
```

---

## CORS Error

The FastAPI backend allows the Vite frontend:

```text
http://localhost:5173
```

If the frontend runs on another port, update the CORS configuration in:

```text
backend/app/main.py
```

---

# 🗺️ Roadmap

Future improvements can include:

- [ ] Azure OpenAI integration
- [ ] Natural language agent with tool calling
- [ ] Jenkins integration
- [ ] GitHub / GitLab integration
- [ ] CI/CD pipeline failure analysis
- [ ] Real-time Kubernetes monitoring
- [ ] Automated incident remediation
- [ ] Slack / Microsoft Teams notifications
- [ ] RAG-based runbook search
- [ ] Historical incident analysis
- [ ] Root cause correlation across multiple services
- [ ] Authentication and role-based access
- [ ] Deploy the entire application to Kubernetes

---

# ⚠️ Demo Notes

This project is intended for:

- Learning
- Code Camps
- DevOps demonstrations
- AI + DevOps experiments
- Local development

The current local AI provider uses deterministic rule-based analysis to simulate AI-assisted reasoning.

For a production implementation, the provider can be replaced with Azure OpenAI or another supported LLM provider.

---

# 💡 Key Concept

The goal of this project is not to replace existing DevOps tools.

Instead, the DevOps AI Assistant acts as an intelligent layer on top of existing systems.

```text
Existing DevOps Tools
        +
Kubernetes / CI/CD / IaC
        +
AI Reasoning
        ↓
Faster Investigation
Better Recommendations
Improved Engineering Productivity
```

---

# 📸 Suggested Demo Flow

For a live presentation:

```text
1. Start Docker Desktop
          ↓
2. Start Minikube
          ↓
3. Deploy the broken demo-app
          ↓
4. Start FastAPI backend
          ↓
5. Start React frontend
          ↓
6. Open DevOps AI Dashboard
          ↓
7. Demonstrate Kubernetes Assistant
          ↓
8. Investigate demo incident
          ↓
9. Review Deployment YAML
          ↓
10. Review Terraform / IaC
```

---

# 🤝 Contributing

This project is designed as an experimental DevOps AI platform.

Possible contributions include:

- Additional DevOps tools
- More Kubernetes analysis capabilities
- CI/CD integrations
- Azure OpenAI provider
- Additional IaC engines
- Automated remediation workflows
- UI improvements

---

# 📄 License

This project is intended for educational and demonstration purposes.

---

# 🚀 Final Summary

The DevOps AI Assistant demonstrates how AI can be integrated into modern DevOps workflows.

The demo currently supports:

✅ Kubernetes cluster inspection

✅ Incident investigation

✅ Kubernetes log analysis

✅ CrashLoopBackOff detection

✅ Root cause analysis

✅ Deployment configuration review

✅ Infrastructure as Code review

✅ Local offline execution

🔜 Azure OpenAI integration

🔜 Automated remediation

🔜 CI/CD integrations

---

Built as a hands-on demonstration of **AI-driven DevOps automation and operational intelligence**.