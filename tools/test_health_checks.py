"""Test Docker Compose health checks.

This script verifies the health of all services in the docker-compose
setup by checking their health status through Docker's health check system.
"""

import argparse
import asyncio
import os
import sys
import time
from typing import Dict, List, Optional, Tuple
import subprocess
import json

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Test Docker Compose health checks")
    parser.add_argument(
        "--compose-file",
        default="./infrastructure/docker/docker-compose.yml",
        help="Path to docker-compose.yml file"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Maximum time to wait for services to be healthy (seconds)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Polling interval to check service health (seconds)"
    )
    return parser.parse_args()

def get_service_health(service_name: str) -> Tuple[str, Optional[str]]:
    """Check the health status of a Docker service.

    Args:
        service_name: Name of the Docker Compose service

    Returns:
        Tuple of (status, details) where status is one of:
        "healthy", "unhealthy", "starting", "none" (no health check)
    """
    try:
        # Get container ID for the service
        cmd = f"docker-compose ps -q {service_name}"
        container_id = subprocess.check_output(cmd, shell=True).decode().strip()

        if not container_id:
            return "not_found", f"Service '{service_name}' not found or not running"

        # Get container health status
        cmd = f"docker inspect --format='{{{{json .State.Health}}}}' {container_id}"
        result = subprocess.check_output(cmd, shell=True).decode().strip()

        if result == "<no value>":
            # Container has no health check
            return "none", None

        health_data = json.loads(result)
        status = health_data.get("Status", "unknown")

        if status == "healthy":
            return "healthy", None
        elif status == "unhealthy":
            # Get the last health check log for more details
            logs = health_data.get("Log", [])
            if logs:
                last_log = logs[-1]
                return "unhealthy", last_log.get("Output", "No details available")
            return "unhealthy", "No details available"
        else:
            return status, None

    except subprocess.CalledProcessError as e:
        return "error", f"Error checking service health: {str(e)}"
    except Exception as e:
        return "error", f"Unexpected error: {str(e)}"

def get_all_services(compose_file: str) -> List[str]:
    """Get list of all services defined in the docker-compose file.

    Args:
        compose_file: Path to docker-compose.yml file

    Returns:
        List of service names
    """
    try:
        cmd = f"docker-compose -f {compose_file} config --services"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return output.split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Error getting services: {str(e)}")
        sys.exit(1)

def print_health_status(services_health: Dict[str, Tuple[str, Optional[str]]]) -> None:
    """Print the health status of all services in a formatted table.

    Args:
        services_health: Dictionary mapping service names to health status
    """
    # Calculate column widths
    service_width = max(len(service) for service in services_health.keys()) + 2
    status_width = 12  # Enough for the longest status

    # Print header
    print("\n" + "=" * (service_width + status_width + 4))
    print(f"| {'Service'.ljust(service_width)} | {'Status'.ljust(status_width)} |")
    print("|" + "-" * (service_width + 2) + "|" + "-" * (status_width + 2) + "|")

    # Print rows
    for service, (status, _) in services_health.items():
        # Color status based on value
        if status == "healthy":
            status_str = f"\033[92m{status}\033[0m"  # Green
        elif status == "unhealthy":
            status_str = f"\033[91m{status}\033[0m"  # Red
        elif status == "starting":
            status_str = f"\033[93m{status}\033[0m"  # Yellow
        elif status == "none":
            status_str = f"\033[94mno check\033[0m"  # Blue
        else:
            status_str = f"\033[90m{status}\033[0m"  # Gray

        print(f"| {service.ljust(service_width)} | {status_str.ljust(status_width)} |")

    print("=" * (service_width + status_width + 4))

    # Print details for unhealthy services
    for service, (status, details) in services_health.items():
        if status == "unhealthy" and details:
            print(f"\n\033[91mUnhealthy service '{service}' details:\033[0m")
            print(f"  {details}")

def main() -> None:
    """Run the health check test."""
    args = parse_args()

    # Validate docker-compose file
    if not os.path.exists(args.compose_file):
        print(f"Error: Docker Compose file not found at {args.compose_file}")
        sys.exit(1)

    # Get all services
    services = get_all_services(args.compose_file)
    print(f"Found {len(services)} services in docker-compose.yml")

    # Test services health
    start_time = time.time()
    all_healthy = False

    try:
        print(f"Waiting up to {args.timeout} seconds for all services to be healthy...")

        while time.time() - start_time < args.timeout:
            services_health = {service: get_service_health(service) for service in services}
            print_health_status(services_health)

            # Check if all services are healthy or have no health check
            statuses = [status for status, _ in services_health.values()]
            if all(status in ["healthy", "none"] for status in statuses):
                all_healthy = True
                print("\n✅ All services are healthy or don't have health checks!")
                break

            # Check if any service is unhealthy (terminal state)
            if any(status == "unhealthy" for status, _ in services_health.values()):
                print("\n❌ Some services are unhealthy. Check the details above.")
                sys.exit(1)

            # Wait before checking again
            print(f"\nWaiting {args.interval} seconds before checking again...")
            time.sleep(args.interval)

        if not all_healthy:
            print("\n❌ Timed out waiting for services to become healthy")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(130)

if __name__ == "__main__":
    main()
