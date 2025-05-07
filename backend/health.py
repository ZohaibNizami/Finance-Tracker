from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
