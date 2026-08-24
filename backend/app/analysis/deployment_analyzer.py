def analyze_deployment(
    deployment: str,
) -> dict:

    findings = []

    text = deployment.lower()

    if "resources:" not in text:
        findings.append(
            "CPU and memory resources are not defined."
        )

    if "readinessprobe:" not in text:
        findings.append(
            "Readiness probe is missing."
        )

    if "livenessprobe:" not in text:
        findings.append(
            "Liveness probe is missing."
        )

    if "replicas: 1" in text:
        findings.append(
            "Only one replica is configured."
        )

    return {
        "findings": findings,
        "status": (
            "NEEDS_IMPROVEMENT"
            if findings
            else "GOOD"
        ),
    }