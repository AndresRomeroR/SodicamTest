from fastapi import APIRouter

from api.response.api_response import ApiResponse

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("", summary="Health Check", response_model=ApiResponse)
async def health_check_all():
    return ApiResponse.create_successful(
        result={"status": "ok", "service": "etq-print-api"},
        meta=None,
        messages=None,
    )
