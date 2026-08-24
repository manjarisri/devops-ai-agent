from typing import Any

import docker


def get_docker_client():
    return docker.from_env()


def get_containers() -> list[dict[str, Any]]:
    """
    Return Docker containers.
    """

    try:
        client = get_docker_client()

        containers = client.containers.list(
            all=True
        )

        return [
            {
                "id": container.short_id,
                "name": container.name,
                "image": (
                    container.image.tags
                    if container.image
                    else []
                ),
                "status": container.status,
            }
            for container in containers
        ]

    except Exception as exc:
        raise RuntimeError(
            f"Docker error: {str(exc)}"
        )


def get_docker_images() -> list[dict[str, Any]]:
    """
    Return Docker images.
    """

    try:
        client = get_docker_client()

        images = client.images.list()

        return [
            {
                "id": image.short_id,
                "tags": image.tags,
                "created": image.attrs.get("Created"),
            }
            for image in images
        ]

    except Exception as exc:
        raise RuntimeError(
            f"Docker error: {str(exc)}"
        )