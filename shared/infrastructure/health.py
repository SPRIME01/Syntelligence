"""Health check utilities for microservices.

This module provides reusable health check functions for monitoring
service and dependency health status.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Callable, Awaitable, Optional, Union

logger = logging.getLogger(__name__)

class HealthStatus:
    """Health status enum-like constants."""
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"

class HealthCheck:
    """Health check implementation for microservices.

    Provides methods to register and execute health checks for
    service dependencies like databases, message brokers, and other services.
    """

    def __init__(self, service_name: str):
        """Initialize the health check manager.

        Args:
            service_name: The name of the service using this health check
        """
        self.service_name = service_name
        self.checks: Dict[str, Callable[[], Awaitable[Dict[str, Any]]]] = {}
        self.last_check_time: Optional[datetime] = None

    def register_check(self, name: str, check_func: Callable[[], Awaitable[Dict[str, Any]]]) -> None:
        """Register a health check function.

        Args:
            name: Name of the dependency to check
            check_func: Async function that performs the health check and returns status
        """
        self.checks[name] = check_func

    async def check_health(self) -> Dict[str, Any]:
        """Execute all registered health checks and return aggregated status.

        Returns:
            Health check response with service status and dependency details
        """
        self.last_check_time = datetime.utcnow()
        check_time_iso = self.last_check_time.isoformat() + "Z"

        results = {}
        overall_status = HealthStatus.UP

        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[name] = result

                # Update overall status based on dependency status
                if result.get("status") == HealthStatus.DOWN:
                    overall_status = HealthStatus.DOWN
                elif result.get("status") == HealthStatus.DEGRADED and overall_status != HealthStatus.DOWN:
                    overall_status = HealthStatus.DEGRADED

            except Exception as e:
                logger.exception(f"Health check for {name} failed")
                results[name] = {
                    "status": HealthStatus.DOWN,
                    "error": str(e)
                }
                overall_status = HealthStatus.DOWN

        return {
            "service": self.service_name,
            "status": overall_status,
            "timestamp": check_time_iso,
            "dependencies": results
        }

# Common health check implementations for different dependencies

async def check_mongodb(uri: str, timeout: float = 5.0) -> Dict[str, Any]:
    """Check MongoDB connection health.

    Args:
        uri: MongoDB connection URI
        timeout: Connection timeout in seconds

    Returns:
        Health check result
    """
    try:
        import motor.motor_asyncio

        client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=int(timeout * 1000)
        )
        await client.admin.command('ping')

        return {
            "status": HealthStatus.UP
        }
    except Exception as e:
        return {
            "status": HealthStatus.DOWN,
            "error": str(e)
        }

async def check_postgres(uri: str, timeout: float = 5.0) -> Dict[str, Any]:
    """Check PostgreSQL connection health.

    Args:
        uri: PostgreSQL connection URI
        timeout: Connection timeout in seconds

    Returns:
        Health check result
    """
    try:
        import asyncpg

        conn = await asyncpg.connect(uri, timeout=timeout)
        await conn.execute('SELECT 1')
        await conn.close()

        return {
            "status": HealthStatus.UP
        }
    except Exception as e:
        return {
            "status": HealthStatus.DOWN,
            "error": str(e)
        }

async def check_rabbitmq(uri: str, timeout: float = 5.0) -> Dict[str, Any]:
    """Check RabbitMQ connection health.

    Args:
        uri: RabbitMQ connection URI
        timeout: Connection timeout in seconds

    Returns:
        Health check result
    """
    try:
        import aio_pika

        connection = await aio_pika.connect_robust(
            uri,
            timeout=timeout
        )
        await connection.close()

        return {
            "status": HealthStatus.UP
        }
    except Exception as e:
        return {
            "status": HealthStatus.DOWN,
            "error": str(e)
        }

async def check_arango(uri: str, username: str, password: str,
                        database: str, timeout: float = 5.0) -> Dict[str, Any]:
    """Check ArangoDB connection health.

    Args:
        uri: ArangoDB connection URI
        username: ArangoDB username
        password: ArangoDB password
        database: ArangoDB database name
        timeout: Connection timeout in seconds

    Returns:
        Health check result
    """
    try:
        from aioarangodb import ArangoClient

        client = ArangoClient(hosts=uri)
        db = await client.db(database, username=username, password=password)
        await db.ping()

        return {
            "status": HealthStatus.UP
        }
    except Exception as e:
        return {
            "status": HealthStatus.DOWN,
            "error": str(e)
        }

async def check_http_endpoint(url: str, timeout: float = 5.0) -> Dict[str, Any]:
    """Check HTTP endpoint health.

    Args:
        url: HTTP endpoint URL to check
        timeout: Request timeout in seconds

    Returns:
        Health check result
    """
    try:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status < 400:
                    return {
                        "status": HealthStatus.UP,
                        "statusCode": response.status
                    }
                else:
                    return {
                        "status": HealthStatus.DOWN,
                        "statusCode": response.status
                    }
    except Exception as e:
        return {
            "status": HealthStatus.DOWN,
            "error": str(e)
        }
