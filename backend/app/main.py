"""Main application module.

This module configures and creates the FastAPI application instance.
It includes routes, middleware, exception handlers, and API documentation.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

# Import API routers
from app.api.v1.endpoints.users import router as users_router

# Create FastAPI application
app = FastAPI(
    title="Syntelligence API",
    description="""
    Syntelligence API provides a comprehensive interface for interacting with the platform.

    ## Features

    * **User Management** - Create and manage user accounts
    * **Project Management** - Create, update, and collaborate on projects
    * **Authentication** - Secure token-based authentication

    ## Interactive Documentation

    * Swagger UI: [/docs](/docs)
    * ReDoc: [/redoc](/redoc)
    """,
    version="0.1.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you would set specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router, prefix="/api/v1")

# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for all unhandled exceptions.

    Args:
        request: The request that caused the exception
        exc: The exception raised

    Returns:
        A JSON response with error details
    """
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

# Custom OpenAPI schema with enhanced documentation
def custom_openapi():
    """Generate custom OpenAPI schema with enhanced documentation.

    Returns:
        The OpenAPI schema dictionary
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add custom documentation enhancements here if needed
    # For example, add security schemes, examples, etc.

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom documentation endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Serve custom Swagger UI.

    Returns:
        HTML response with Swagger UI
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    """Serve custom ReDoc.

    Returns:
        HTML response with ReDoc
    """
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Check the health of the application.

    This endpoint can be used by monitoring systems to verify that
    the API is running and responding to requests.

    Returns:
        Dictionary with status information
    """
    return {"status": "healthy", "version": app.version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
