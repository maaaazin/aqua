from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def generate_tests(url: str):
    """
    Generate tests for a given webpage
    """

    return {
        "url": url,
        "message": "Test generation started"
    }