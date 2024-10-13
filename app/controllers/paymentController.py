from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.paymentService import PaymentService
from app.helpers.exception import PaymentException
from app.models.paymentBaseModel import PaymentMutation

router = APIRouter()
payment_service = PaymentService()

# Correct route paths with leading slashes
@router.post("/{userId}")
async def createPaymentDetails(paymentMutation: PaymentMutation, userId: str):
    try:
        
        response = payment_service.createPaymentDetail(paymentMutation, userId)
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payment created successfully", 
            "paymentId": response["paymentId"]
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/payments")
async def retrievePaymentDetail():
    try:

        # Call the instance method getPaymentList()
        response = payment_service.getPaymentList()
        
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payments fetched successfully", 
            "payments": response["payments"]  # Corrected key from "restaurants" to "payments"
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{paymentId}")
async def getAccountFromSystem(paymentId: str):
    try:
        response = payment_service.getPaymentById(paymentId)

        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payment fetched successfully", 
            "payment": response["payment"]
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.put("/{paymentId}/update")
async def updateUserPaymentDetail(paymentMutation: PaymentMutation, paymentId: str):
    try:
        response = payment_service.updatePayment(paymentMutation, paymentId)
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payment updated successfully", 
            "paymentId": response["paymentId"]
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
