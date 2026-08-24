from app.tools.kubernetes import (
    get_pods,
    get_pod_logs,
    get_pod_events,
    get_deployments,
    get_services,
)


DEVOPS_TOOLS = {
    "get_pods": get_pods,
    "get_pod_logs": get_pod_logs,
    "get_pod_events": get_pod_events,
    "get_deployments": get_deployments,
    "get_services": get_services,
}