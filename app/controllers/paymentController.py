from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.paymentService import PaymentService
from app.helpers.exception import PaymentException
from app.models.paymentBaseModel import PaymentMutation

router = APIRouter()
payment_service = PaymentService()

# Correct route paths with leading slashes
@router.post("/{userId}/create")
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
async def retrieveAllPaymentDetail():
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

@router.get("/payments/{userId}")
async def retrievePaymentDetailByUserID(userId: str):
    try:

        # Call the instance method getPaymentList()
        response = payment_service.getAllPaymentsByUserId(userId)
        print(response)
        
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payments fetched successfully", 
            "payments": response["payments"]  # Corrected key from "restaurants" to "payments"
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/payments/singlePayment/{paymentId}")
async def retrievePaymentDetailByPaymentID(paymentId: str):
    try:
        
        response = payment_service.getPaymentByPaymentId(paymentId)
        
        
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payments fetched successfully", 
            "payment": response["payment"]  # Corrected key from "restaurants" to "payments"
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/account/{paymentId}")
async def getAccountFromSystemByPaymentId(paymentId: str):
    try:
        response = payment_service.getAccountInPaymentFromSystemByPaymentId(paymentId)
        
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payment fetched successfully", 
            "account": response["account"]
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

@router.delete("/{userId}/delete/{paymentId}")
async def deleteUserPaymentDetail(userId: str, paymentId: str):
    try:
        response = payment_service.deletePayment(userId, paymentId)
        return JSONResponse(status_code=response["statusCode"], content={
            "message": "Payment deleted successfully"
        })
    except PaymentException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")