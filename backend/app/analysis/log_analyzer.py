def analyze_logs(logs: str) -> dict:

    if not logs:
        return {
            "error_detected": False,
            "summary": "No logs were returned.",
            "signals": [],
        }

    text = logs.lower()

    signals = []

    patterns = {
        "connection_refused": [
            "connection refused",
            "connect: connection refused",
        ],
        "database_error": [
            "database",
            "db connection",
            "postgres",
            "mysql",
            "mongodb",
        ],
        "timeout": [
            "timeout",
            "timed out",
        ],
        "authentication_error": [
            "authentication failed",
            "unauthorized",
            "invalid password",
            "access denied",
        ],
        "configuration_error": [
            "configuration",
            "config error",
            "missing environment",
            "environment variable",
        ],
    }

    for signal, keywords in patterns.items():

        if any(
            keyword in text
            for keyword in keywords
        ):
            signals.append(signal)

    error_words = [
        "error",
        "exception",
        "fatal",
        "failed",
        "failure",
        "panic",
        "refused",
    ]

    has_error = any(
        word in text
        for word in error_words
    )

    return {
        "error_detected": (
            has_error or bool(signals)
        ),
        "signals": signals,
        "summary": build_summary(signals),
    }


def build_summary(
    signals: list[str],
) -> str:

    if "connection_refused" in signals:
        return (
            "The application appears unable to connect "
            "to a required service."
        )

    if "database_error" in signals:
        return (
            "The logs indicate a possible database "
            "connectivity problem."
        )

    if "timeout" in signals:
        return (
            "The application appears to be "
            "experiencing a timeout."
        )

    if "authentication_error" in signals:
        return (
            "The logs indicate an authentication "
            "or authorization failure."
        )

    if "configuration_error" in signals:
        return (
            "The logs indicate a configuration problem."
        )

    if signals:
        return (
            "The logs contain error signals that "
            "require investigation."
        )

    return (
        "No obvious error pattern was detected."
    )