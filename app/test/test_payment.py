from fastapi.testclient import TestClient
from app.helpers.exception import PaymentException
from main import app 
from unittest.mock import patch

client = TestClient(app)

def test_createPaymentDetails_ReturnSuccess():
    userId = "userId123"
    paymentData = {
        "paymentDate": "2024-10-08T09:00:00",
        "paymentAmount": 100.0,
        "paymentStatus": "completed",
        "paymentMethod": "credit_card",
        "paymentCurrency": "USD",
        "paymentType": "one-time",
        "paymentDescription": "Payment for order #123",
        "AccountID": "account123",
        "AccountName": "Good Eats Account",
        "AccountType": "business",
        "AccountNumber": "123456789",
        "AccountBalance": 1000.0,
        "AccountStatus": "active",
        "AccountCurrency": "USD",
        "AccountLimit": 5000.0,
    }
    
    response = client.post(f"/api/payment/{userId}", json=paymentData)

    assert response.status_code == 201
    assert "paymentId" in response.json()

def test_createPaymentDetails_InvalidData_ReturnError():
    userId = "userId123"
    paymentData = {
        "paymentDate": "2024-10-08T09:00:00",
        "paymentAmount": -100.0,  # Invalid amount
        "paymentStatus": "completed",
        "paymentMethod": "credit_card",
        "paymentCurrency": "USD",
        "paymentType": "one-time",
        "paymentDescription": "Payment for order #123",
        "AccountID": "account123",
        "AccountName": "Good Eats Account",
        "AccountType": "business",
        "AccountNumber": "123456789",
        "AccountBalance": 1000.0,
        "AccountStatus": "active",
        "AccountCurrency": "USD",
        "AccountLimit": 5000.0,
    }

    response = client.post(f"/api/payment/{userId}", json=paymentData)

    assert response.status_code == 400
    assert response.json()["detail"] == "Payment amount must be a positive number."

def test_retrievePaymentList_ReturnSuccess():
    mockResponse = {
        "statusCode": 200,
        "payments": [
            {
                "paymentId": "payment123",
                "paymentDate": "2024-10-08T09:00:00",
                "paymentAmount": 100.0,
                "paymentStatus": "completed",
                "paymentMethod": "credit_card",
                "paymentCurrency": "USD",
                "paymentType": "one-time",
                "paymentDescription": "Payment for order #123",
                "AccountID": "account123",
                "AccountName": "Good Eats Account",
                "AccountType": "business",
                "AccountNumber": "123456789",
                "AccountBalance": 1000.0,
                "AccountStatus": "active",
                "AccountCurrency": "USD",
                "AccountLimit": 5000.0,
                "created_at": "2024-10-08T09:00:00",
                "updated_at": "2024-10-08T09:00:00",
            }
        ]
    }

    with patch('app.services.paymentService.PaymentService.getPaymentList', return_value=mockResponse):
        response = client.get("/api/payment/payments")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Payments fetched successfully",
        "payments": mockResponse["payments"]
    }

def test_retrievePaymentList_ReturnFailure():
    mockException = PaymentException(500, "Error fetching payment list.")

    with patch('app.services.paymentService.PaymentService.getPaymentList', side_effect=mockException):
        response = client.get("/api/payment/payments")

    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching payment list."}

def test_retrievePaymentById_ReturnSuccess():
    paymentId = "payment123"
    mockResponse = {
        "statusCode": 200,
        "payment": {
            "paymentId": paymentId,
            "paymentDate": "2024-10-08T09:00:00",
            "paymentAmount": 100.0,
            "paymentStatus": "completed",
            "paymentMethod": "credit_card",
            "paymentCurrency": "USD",
            "paymentType": "one-time",
            "paymentDescription": "Payment for order #123",
            "AccountID": "account123",
            "AccountName": "Good Eats Account",
            "AccountType": "business",
            "AccountNumber": "123456789",
            "AccountBalance": 1000.0,
            "AccountStatus": "active",
            "AccountCurrency": "USD",
            "AccountLimit": 5000.0,
            "created_at": "2024-10-08T09:00:00",
            "updated_at": "2024-10-08T09:00:00",
        }
    }
    
    with patch('app.services.paymentService.PaymentService.getPaymentById', return_value=mockResponse):
        response = client.get(f"/api/payment/{paymentId}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Payment fetched successfully",
        "payment": mockResponse["payment"]
    }

def test_retrievePaymentById_ReturnFailure():
    paymentId = "nonexistent_payment_id"
    mockException = PaymentException(404, "Payment not found.")

    with patch('app.services.paymentService.PaymentService.getPaymentById', side_effect=mockException):
        response = client.get(f"/api/payment/{paymentId}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found."}

def test_updatePayment_ReturnSuccess():
    paymentId = "payment123"
    mockResponse = {
        "statusCode": 200,
        "paymentId": paymentId
    }

    with patch('app.services.paymentService.PaymentService.updatePayment', return_value=mockResponse):
        payment_data = {
            "paymentDate": "2024-10-09T09:00:00",
            "paymentAmount": 150.0,
            "paymentStatus": "completed",
            "paymentMethod": "credit_card",
            "paymentCurrency": "USD",
            "paymentType": "recurring",
            "paymentDescription": "Updated payment for order #123",
            "AccountID": "account123",
            "AccountName": "Good Eats Account",
            "AccountType": "business",
            "AccountNumber": "123456789",
            "AccountBalance": 850.0,
            "AccountStatus": "active",
            "AccountCurrency": "USD",
            "AccountLimit": 5000.0,
        }

        response = client.put(f"/api/payment/{paymentId}/update", json=payment_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Payment updated successfully", "paymentId": paymentId}

def test_updatePayment_ReturnFailure_InvalidData():
    paymentId = "payment123"
    mockException = PaymentException(400, "Payment amount must be a positive number.")

    with patch('app.services.paymentService.PaymentService.updatePayment', side_effect=mockException):
        payment_data = {
            "paymentDate": "2024-10-09T09:00:00",
            "paymentAmount": -150.0,  # Invalid amount
            "paymentStatus": "completed",
            "paymentMethod": "credit_card",
            "paymentCurrency": "USD",
            "paymentType": "recurring",
            "paymentDescription": "Updated payment for order #123",
            "AccountID": "account123",
            "AccountName": "Good Eats Account",
            "AccountType": "business",
            "AccountNumber": "123456789",
            "AccountBalance": 850.0,
            "AccountStatus": "active",
            "AccountCurrency": "USD",
            "AccountLimit": 5000.0,
        }

        response = client.put(f"/api/payment/{paymentId}/update", json=payment_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Payment amount must be a positive number."}

def test_deletePayment_ReturnSuccess():
    paymentId = "payment123"
    mockResponse = {
        "statusCode": 200,
        "paymentId": paymentId
    }

    with patch('app.services.paymentService.PaymentService.deletePayment', return_value=mockResponse):
        response = client.delete(f"/api/payment/{paymentId}/delete")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Payment deleted successfully",
        "paymentId": mockResponse["paymentId"]
    }

def test_deletePayment_ReturnFailure():
    paymentId = "nonexistent_payment_id"
    mockException = PaymentException(404, "Payment not found.")

    with patch('app.services.paymentService.PaymentService.deletePayment', side_effect=mockException):
        response = client.delete(f"/api/payment/{paymentId}/delete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found."}
