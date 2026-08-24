from app.ai.base import AIProvider


class LocalAIProvider(AIProvider):

    def analyze_incident(
        self,
        evidence: dict,
    ) -> dict:

        findings = list(
            evidence.get(
                "findings",
                [],
            )
        )

        logs = evidence.get(
            "logs",
            [],
        )

        recommendations = [
            "Review the application logs.",
            "Review Kubernetes events.",
            "Verify application dependencies.",
            "Check deployment configuration.",
        ]

        root_cause = (
            "Unable to determine root cause."
        )

        confidence = 0.50

        evidence_text = str(evidence).lower()

        # ------------------------------------------------
        # Check analyzed log signals
        # ------------------------------------------------

        for log in logs:

            analysis = log.get(
                "analysis",
                {},
            )

            signals = analysis.get(
                "signals",
                [],
            )

            if "database_error" in signals:

                root_cause = (
                    "The application is failing during startup "
                    "because it cannot resolve or connect to its "
                    "required database dependency. The database "
                    "connectivity failure causes the container to "
                    "exit repeatedly, resulting in CrashLoopBackOff."
                )

                confidence = 0.95

                findings.append(
                    "Database connectivity or DNS resolution "
                    "failure detected in application logs."
                )

                recommendations.extend([
                    "Verify the database hostname and connection configuration.",
                    "Verify Kubernetes Service and DNS resolution for the database.",
                    "Verify required environment variables and secrets.",
                    "Confirm the database service is reachable from the application pod.",
                ])

            elif "connection_refused" in signals:

                root_cause = (
                    "The application cannot connect to a required "
                    "service. The logs indicate a connection "
                    "refused error, causing the application to fail."
                )

                confidence = 0.90

        # ------------------------------------------------
        # Check raw Kubernetes / log evidence
        # ------------------------------------------------

        if (
            root_cause == "Unable to determine root cause."
            and (
                "socket.gaierror" in evidence_text
                or "getaddrinfo" in evidence_text
                or "connecting to database" in evidence_text
            )
        ):

            root_cause = (
                "The application is failing because it cannot "
                "resolve the hostname of its required database "
                "dependency. The DNS resolution failure causes "
                "the application to exit repeatedly."
            )

            confidence = 0.95

        # ------------------------------------------------
        # Check CrashLoopBackOff
        # ------------------------------------------------

        if (
            "crashloopbackoff" in evidence_text
            or "back-off restarting failed container" in evidence_text
        ):

            findings.append(
                "Kubernetes detected repeated container failures "
                "and placed the workload into CrashLoopBackOff."
            )

            recommendations.append(
                "Inspect the previous container logs to identify "
                "the startup failure."
            )

        # ------------------------------------------------
        # Check deployment availability
        # ------------------------------------------------

        for deployment in evidence.get(
            "deployments",
            [],
        ):

            desired = deployment.get(
                "desired_replicas",
                0,
            )

            available = deployment.get(
                "available_replicas",
                0,
            )

            if desired > 0 and available == 0:

                findings.append(
                    f"Deployment {deployment.get('name')} has "
                    f"{desired} desired replicas but "
                    f"{available} available replicas."
                )

        # Remove duplicate entries
        findings = list(dict.fromkeys(findings))
        recommendations = list(
            dict.fromkeys(recommendations)
        )

        return {
            "status": evidence.get(
                "status",
                "UNKNOWN",
            ),
            "severity": evidence.get(
                "severity",
                "UNKNOWN",
            ),
            "root_cause": root_cause,
            "findings": findings,
            "recommendations": recommendations,
            "confidence": confidence,
            "provider": "local-demo",
        }

    def review_deployment(
        self,
        deployment: str,
    ) -> dict:

        recommendations = []

        text = deployment.lower()

        if "resources:" not in text:

            recommendations.append(
                "Add CPU and memory requests "
                "and limits."
            )

        if "livenessprobe:" not in text:

            recommendations.append(
                "Consider adding a liveness probe."
            )

        if "readinessprobe:" not in text:

            recommendations.append(
                "Consider adding a readiness probe."
            )

        if "replicas: 1" in text:

            recommendations.append(
                "Consider multiple replicas "
                "for high availability."
            )

        return {
            "provider": "local-demo",
            "recommendations": recommendations,
        }

    def review_iac(
        self,
        content: str,
        iac_type: str,
    ) -> dict:

        recommendations = []

        text = content.lower()

        if "password" in text:

            recommendations.append(
                "Avoid hard-coded passwords or secrets."
            )

        if "0.0.0.0/0" in text:

            recommendations.append(
                "Review unrestricted network access."
            )

        if "latest" in text:

            recommendations.append(
                "Avoid mutable 'latest' image tags."
            )

        return {
            "provider": "local-demo",
            "iac_type": iac_type,
            "recommendations": recommendations,
        }


# ============================================================
# AZURE OPENAI FUTURE
# ============================================================
#
# Later create:
#
# AzureOpenAIProvider(AIProvider)
#
# using the same methods:
#
#   analyze_incident()
#   review_deployment()
#   review_iac()
#
# The rest of the application will not need to change.
# ============================================================