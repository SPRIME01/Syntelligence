# Syntelligence Tools

This directory contains utility tools and scripts for development, testing, and operations.

## Testing Docker Compose Health Checks

The `test_health_checks.py` script tests the health status of all services in the Docker Compose setup.

### Prerequisites

- Docker and Docker Compose installed
- All containers started with `docker-compose up`

### Usage

```bash
# From the project root
python tools/test_health_checks.py

# With custom options
python tools/test_health_checks.py --compose-file ./path/to/docker-compose.yml --timeout 600 --interval 15
```

### Options

- `--compose-file`: Path to the docker-compose.yml file (default: `./infrastructure/docker/docker-compose.yml`)
- `--timeout`: Maximum time to wait for services to be healthy in seconds (default: 300)
- `--interval`: Polling interval to check service health in seconds (default: 10)

### Output

The script will display a table showing the health status of each service:

```
=============================
| Service      | Status     |
|--------------|------------|
| api-gateway  | healthy    |
| mongodb      | healthy    |
| postgres     | healthy    |
| rabbitmq     | starting   |
| arangodb     | no check   |
=============================
```

If any service is unhealthy, the script will display details about the failure.

## Updating the Action Plan

To update the action plan with completed items:

1. Edit `action_plan.md`
2. Change `[ ]` to `[x]` for completed tasks
3. Commit the changes
