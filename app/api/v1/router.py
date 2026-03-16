from fastapi import APIRouter

from app.api.v1 import test_generation
from app.api.v1 import test_execution
from app.api.v1 import test_cases
from app.api.v1 import projects
from app.api.v1 import llm

router = APIRouter()

router.include_router(
    test_generation.router,
    prefix="/generate",
    tags=["Test Generation"],
)

router.include_router(
    test_execution.router,
    prefix="/execute",
    tags=["Test Execution"],
)

router.include_router(
    test_cases.router,
    prefix="/test-cases",
    tags=["Test Cases"],
)

router.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"],
)

router.include_router(
    llm.router,
    prefix="/llm",
    tags=["LLM"],
)