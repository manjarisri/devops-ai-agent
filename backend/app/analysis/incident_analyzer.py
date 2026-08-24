from app.tools.kubernetes import (
    get_pods,
    get_pod_logs,
    get_pod_events,
    get_deployments,
)

from app.analysis.log_analyzer import (
    analyze_logs,
)


def investigate_application(
    app_name: str,
    namespace: str = "default",
) -> dict:

    pods = get_pods(namespace)
    deployments = get_deployments(namespace)

    matching_pods = [
        pod
        for pod in pods
        if app_name in pod["name"]
    ]

    incident = {
        "application": app_name,
        "namespace": namespace,
        "status": "UNKNOWN",
        "severity": "UNKNOWN",
        "pods": matching_pods,
        "deployments": deployments,
        "logs": [],
        "events": [],
        "findings": [],
        "recommendations": [],
    }

    if not matching_pods:

        incident["status"] = "NOT_FOUND"
        incident["severity"] = "INFO"

        incident["findings"].append(
            f"No pods found matching "
            f"application '{app_name}'."
        )

        return incident

    has_failure = False

    for pod in matching_pods:

        pod_name = pod["name"]

        events = get_pod_events(
            pod_name=pod_name,
            namespace=namespace,
        )

        incident["events"].extend(events)

        logs = get_pod_logs(
            pod_name=pod_name,
            namespace=namespace,
        )

        log_analysis = analyze_logs(logs)

        incident["logs"].append(
            {
                "pod": pod_name,
                "analysis": log_analysis,
                "raw_logs": logs,
            }
        )

        if log_analysis["error_detected"]:

            has_failure = True

            incident["findings"].append(
                f"Errors detected in pod "
                f"{pod_name}: "
                f"{log_analysis['summary']}"
            )

        for container in pod.get(
            "containers",
            [],
        ):

            state = container.get(
                "state",
                "",
            )

            failure_states = [
                "waiting:CrashLoopBackOff",
                "waiting:Error",
                "terminated:Error",
                "terminated:CrashLoopBackOff",
            ]

            if any(
                failure in state
                for failure in failure_states
            ):

                has_failure = True

                incident["findings"].append(
                    f"Container "
                    f"{container['name']} in "
                    f"{pod_name} is unhealthy: "
                    f"{state}"
                )

    if has_failure:

        incident["status"] = "UNHEALTHY"
        incident["severity"] = "HIGH"

        incident["recommendations"] = [
            "Review the application logs.",
            "Review Kubernetes events.",
            "Check application dependencies.",
            "Check deployment configuration.",
            "Verify required services are available.",
        ]

    else:

        incident["status"] = "HEALTHY"
        incident["severity"] = "INFO"

    return incident