from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.paymentService import PaymentService
from app.helpers.exception import PaymentException
from app.models.paymentBaseModel import PaymentMutation

router = APIRouter()
paymentService = PaymentService()

@router.post("/{userId}/create")
async def createPaymentDetails(paymentMutation: PaymentMutation, userId: str):
    try:
        response = paymentService.createPaymentDetail(paymentMutation, userId)
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payment created successfully", 
            "paymentId": response["paymentId"]
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/payments/{userId}")
async def retrievePaymentDetailByUserID(userId: str):
    try:
        response = paymentService.getPaymentByUserId(userId)        
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payments fetched successfully", 
            "payment": response["payment"]
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

