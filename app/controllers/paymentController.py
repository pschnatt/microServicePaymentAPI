from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.helpers.exception import PaymentException
from app.models.paymentBaseModel import PaymentMutation
from app.services.paymentService import PaymentService

router = APIRouter()

PaymentMutation = PaymentService()

@router.post("/{userId}/create")
async def createPaymentDetails(paymentMutation : PaymentMutation, userId: str):
    try:
      response = PaymentService.createPaymentDetail(paymentMutation, userId)
      return JSONResponse(status_code=response["statusCode"], content={"message": "Payment created successfully", "paymentId": response["paymentId"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get")
async def retrievePaymentDetail():
    try:
        response = PaymentService.getPaymentList()
        return JSONResponse(status_code=response["statusCode"], content={"message": "Payments fetched successfully", "restaurants": response["restaurants"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get/{paymentId}")
async def retrievePaymentById(paymentId: str):
    try:
        response = PaymentService.getPaymentById(paymentId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Payment fetched successfully", "payment": response["payment"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{userId}/update/{restaurantId}")
async def updateUserPaymentDetail(paymentMutation : PaymentMutation, restaurantId: str, userId : str):
    try:
        response = PaymentService.updatePayment(paymentMutation, restaurantId, userId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant updated successfully", "restaurantId": response["restaurantId"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.delete("/{userId}/delete/{restaurantId}")
# async def deletePayment(restaurantId: str, userId: str):
#     try:
#         response = PaymentService.deletePayment(restaurantId, userId)
#         return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant deleted successfully", "restaurantId": response["restaurantId"]})
#     except PaymentException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)
