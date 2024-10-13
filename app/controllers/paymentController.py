from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.helpers.exception import PaymentException
from microServicePaymentAPI.app.models.paymentBaseModel import PaymentMutation
from microServicePaymentAPI.app.services.paymentService import PaymentService

router = APIRouter()

PaymentMutation = PaymentService()

@router.post("/{userId}/create")
async def addPayment(paymentMutation : PaymentMutation, userId: str):
    try:
      response = PaymentService.createPayment(paymentMutation, userId)
      return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant created successfully", "restaurantId": response["restaurantId"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get")
async def retrievePayment():
    try:
        response = PaymentService.getPaymentList()
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurants fetched successfully", "restaurants": response["restaurants"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get/{restaurantId}")
async def retrievePaymentById(restaurantId: str):
    try:
        response = PaymentService.getPaymentById(restaurantId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant fetched successfully", "restaurant": response["restaurant"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{userId}/update/{restaurantId}")
async def updatePayment(paymentMutation : PaymentMutation, restaurantId: str, userId : str):
    try:
        response = PaymentService.updatePayment(paymentMutation, restaurantId, userId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant updated successfully", "restaurantId": response["restaurantId"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{userId}/delete/{restaurantId}")
async def deletePayment(restaurantId: str, userId: str):
    try:
        response = PaymentService.deletePayment(restaurantId, userId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant deleted successfully", "restaurantId": response["restaurantId"]})
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
