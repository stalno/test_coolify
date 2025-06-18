from typing import Annotated
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from src.common.docs import NotFoundError, ForbiddenError, UnAuthorizedError, BadRequest
from src.common.dto import (
    CustomerFilter,
    CustomerCreate,
    CustomerID,
    CreateOrderWithCustomerData,
)
from src.services.user import UserService


api_router = APIRouter(prefix="/api", tags=["Api"])

@api_router.get("/mp")
async def get_mp() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hello World"})

