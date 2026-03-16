from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_test_cases():
    return {"test_cases": []}