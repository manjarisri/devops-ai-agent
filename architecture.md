                         ┌──────────────────────────────┐
                         │          USER                │
                         │                              │
                         │ "Why is my pod failing?"     │
                         └──────────────┬───────────────┘
                                        │
                                        ▼
                    ┌────────────────────────────────────┐
                    │          WEB CHAT UI                │
                    │        React / Next.js              │
                    │                                    │
                    │  Chat │ Cluster │ Deployments       │
                    │       │ Pods    │ Logs              │
                    └────────────────┬───────────────────┘
                                     │
                                     │ REST API
                                     ▼
              ┌──────────────────────────────────────────────┐
              │              DEVOPS AI BACKEND               │
              │                Python / FastAPI              │
              │                                              │
              │  ┌────────────────────────────────────────┐  │
              │  │             AI AGENT                   │  │
              │  │                                        │  │
              │  │ Understand request                     │  │
              │  │ Decide which tool to use               │  │
              │  │ Analyze result                         │  │
              │  │ Generate recommendation                │  │
              │  └───────────────────┬────────────────────┘  │
              │                      │                       │
              │             ┌────────┴────────┐              │
              │             │   TOOL LAYER    │              │
              │             └────────┬─────────┘              │
              │                      │                        │
              │       ┌──────────────┼───────────────┐        │
              │       ▼              ▼               ▼        │
              │   Kubernetes       Docker         Jenkins     │
              │      Tool            Tool           Tool      │
              └───────┬──────────────┬───────────────┬────────┘
                      │              │               │
                      ▼              ▼               ▼
                ┌──────────┐   ┌──────────┐   ┌────────────┐
                │ Minikube │   │  Docker  │   │  Jenkins   │
                │          │   │ Desktop  │   │ (Phase 2)  │
                └──────────┘   └──────────┘   └────────────┘