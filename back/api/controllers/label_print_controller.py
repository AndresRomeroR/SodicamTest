from fastapi import APIRouter, HTTPException, Query, status

from api.response.api_response import ApiResponse
from api.schemas.label_print import LabelPrintRequest
from application.services.print_service import PrintService

label_print_router = APIRouter(prefix="/api/v1/labels", tags=["ETQ Printing"])


@label_print_router.post("/print", response_model=ApiResponse)
async def print_label(request: LabelPrintRequest):
    if not request.identifier.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="lpn or etqId is required")

    result = PrintService().process(
        identifier=request.identifier,
        zone=request.zone,
        requested_by=request.requested_by,
        reprint_reason=request.reprint_reason,
    )
    return ApiResponse.create_successful(result=result, meta=None, messages=None)


@label_print_router.get("/history", response_model=ApiResponse)
async def get_history(identifier: str | None = Query(default=None)):
    return ApiResponse.create_successful(result=PrintService().history(identifier), meta=None, messages=None)
