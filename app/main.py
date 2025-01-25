from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.logging_config import setup_logging
from users.routes import router as users_router

def custom_openapi(app: FastAPI):
    """
    Adds a 'BearerAuth' security scheme to the OpenAPI schema
    so that the Swagger UI can show the 'Authorize' button.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="My API description",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Add global security if you want every endpoint to require it by default
    # openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI()
    app.include_router(users_router)

    # Overwrite the default OpenAPI generation
    app.openapi = lambda: custom_openapi(app)
    return app

app = create_app()
