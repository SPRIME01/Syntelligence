# Architecture Overview

This document provides an overview of the Syntelligence architecture.

## System Architecture

Syntelligence follows a modern, layered architecture that separates concerns and promotes maintainability. The system is built with the following key components:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  Presentation   │─────▶│    Domain       │─────▶│  Infrastructure │
│    Layer        │      │     Layer       │      │     Layer       │
│                 │◀─────│                 │◀─────│                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Presentation Layer

This layer is responsible for handling HTTP requests and responses. It includes:

- **FastAPI** for REST endpoints
- **Strawberry GraphQL** for GraphQL API
- **Swagger UI / ReDoc** for API documentation

### Domain Layer

This layer contains the business logic and domain models:

- **Domain Models** (Pydantic models)
- **Use Cases** (Service layer)
- **Domain Events**
- **Repositories Interfaces**

### Infrastructure Layer

This layer handles external concerns such as:

- **Database Access**
- **External Services**
- **Repository Implementations**
- **Caching**
- **Logging**

## Dependency Injection

The application uses the `dependency-injector` package to implement inversion of control. This approach:

- Decouples components
- Makes testing easier
- Promotes maintainability

## API Documentation

API documentation is automatically generated from:

1. Pydantic model field descriptions
2. FastAPI route docstrings
3. OpenAPI schema

The documentation is accessible via:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **MkDocs**: Static documentation site

## Authentication & Authorization

The system uses JWT token-based authentication with the following flow:

1. User authenticates and receives JWT token
2. Subsequent requests include the token in Authorization header
3. FastAPI dependency validates the token
4. Role-based access control determines permissions

## Error Handling

A global exception handler middleware processes all exceptions:

- **Domain Exceptions**: Mapped to appropriate HTTP status codes
- **Validation Errors**: Converted to 422 Unprocessable Entity responses
- **Unexpected Errors**: Logged and returned as 500 Internal Server Error

## Logging

Structured logging with `structlog` provides context-rich logs:

- Request ID tracking
- User ID tracking (when authenticated)
- Standard format for log shipping
