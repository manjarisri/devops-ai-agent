from kubernetes import client, config
from kubernetes.client.rest import ApiException


def load_kubernetes_config():
    try:
        config.load_kube_config()
    except Exception as exc:
        raise RuntimeError(
            f"Unable to load Kubernetes configuration: {exc}"
        )


def get_core_api():
    load_kubernetes_config()
    return client.CoreV1Api()


def get_apps_api():
    load_kubernetes_config()
    return client.AppsV1Api()


def get_container_state(container):
    if container.state is None:
        return "unknown"

    if container.state.running:
        return "running"

    if container.state.waiting:
        reason = container.state.waiting.reason

        return (
            f"waiting:{reason}"
            if reason
            else "waiting"
        )

    if container.state.terminated:
        reason = container.state.terminated.reason

        return (
            f"terminated:{reason}"
            if reason
            else "terminated"
        )

    return "unknown"


def get_pods(namespace: str = "default"):
    api = get_core_api()

    try:
        pods = api.list_namespaced_pod(
            namespace=namespace
        )

        results = []

        for pod in pods.items:

            container_statuses = []

            if pod.status.container_statuses:

                for container in pod.status.container_statuses:

                    container_statuses.append(
                        {
                            "name": container.name,
                            "ready": container.ready,
                            "restart_count": container.restart_count,
                            "state": get_container_state(
                                container
                            ),
                        }
                    )

            results.append(
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "phase": pod.status.phase,
                    "pod_ip": pod.status.pod_ip,
                    "containers": container_statuses,
                }
            )

        return results

    except ApiException as exc:
        raise RuntimeError(
            f"Kubernetes API error while getting pods: {exc}"
        )


def get_pod_logs(
    pod_name: str,
    namespace: str = "default",
    container: str | None = None,
    tail_lines: int = 100,
):
    api = get_core_api()

    try:
        return api.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container,
            tail_lines=tail_lines,
        )

    except ApiException as exc:
        return f"Unable to retrieve logs: {exc}"


def get_pod_events(
    pod_name: str,
    namespace: str = "default",
):
    api = get_core_api()

    try:
        field_selector = (
            f"involvedObject.name={pod_name}"
        )

        events = api.list_namespaced_event(
            namespace=namespace,
            field_selector=field_selector,
        )

        results = []

        for event in events.items:

            results.append(
                {
                    "reason": event.reason,
                    "message": event.message,
                    "type": event.type,
                    "count": event.count,
                    "first_timestamp": str(
                        event.first_timestamp
                    ),
                    "last_timestamp": str(
                        event.last_timestamp
                    ),
                }
            )

        return results

    except ApiException as exc:
        return [
            {
                "reason": "API_ERROR",
                "message": str(exc),
                "type": "Warning",
            }
        ]


def get_deployments(namespace: str = "default"):
    api = get_apps_api()

    try:
        deployments = api.list_namespaced_deployment(
            namespace=namespace
        )

        results = []

        for deployment in deployments.items:

            results.append(
                {
                    "name": deployment.metadata.name,
                    "namespace": deployment.metadata.namespace,
                    "desired_replicas": (
                        deployment.spec.replicas
                    ),
                    "available_replicas": (
                        deployment.status.available_replicas
                        or 0
                    ),
                    "ready_replicas": (
                        deployment.status.ready_replicas
                        or 0
                    ),
                }
            )

        return results

    except ApiException as exc:
        raise RuntimeError(
            "Kubernetes API error while getting "
            f"deployments: {exc}"
        )


def get_services(namespace: str = "default"):
    api = get_core_api()

    try:
        services = api.list_namespaced_service(
            namespace=namespace
        )

        results = []

        for service in services.items:

            results.append(
                {
                    "name": service.metadata.name,
                    "namespace": service.metadata.namespace,
                    "type": service.spec.type,
                    "cluster_ip": service.spec.cluster_ip,
                    "ports": [
                        {
                            "port": port.port,
                            "target_port": str(
                                port.target_port
                            ),
                            "protocol": port.protocol,
                        }
                        for port in (
                            service.spec.ports or []
                        )
                    ],
                }
            )

        return results

    except ApiException as exc:
        raise RuntimeError(
            "Kubernetes API error while getting "
            f"services: {exc}"
        )