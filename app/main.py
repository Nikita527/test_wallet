import pkgutil
import importlib
from pathlib import Path

from fastapi import FastAPI, APIRouter

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    openapi_url="/openapi.json",
)

api_router = APIRouter()

endpoint_path = Path(__file__).parent / "api" / "endpoints"

template_path = Path(__file__).parent / "api" / "templates"

for module_info in pkgutil.iter_modules([str(endpoint_path)]):
    if not module_info.ispkg:
        module_name = module_info.name
        full_module_name = f"app.api.endpoints.{module_name}"
        module = importlib.import_module(full_module_name)
        if hasattr(module, "router"):
            api_router.include_router(module.router)
        else:
            raise Exception(f"Модуль {module_name} не имеет роутера.")

app.include_router(api_router, prefix=settings.api_prefix)
