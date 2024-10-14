from datetime import datetime
import certifi
from pymongo import MongoClient
from app.helpers.exception import PaymentException
from app.models.paymentBaseModel import PaymentMutation
from app.core.config import settings
from app.helpers.validator import Validator

class PaymentService:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
        self.db = self.client[settings.DB_NAME]
        self.collection = self.db[settings.COLLECTION_NAME]

    def createPaymentDetail(self, paymentMutation : PaymentMutation, userId : str):
      try:
        paymentData = paymentMutation.model_dump()
        paymentData["userId"] = userId
        paymentData["created_by"] = userId
        paymentData["created_at"] = datetime.now().strftime("%d%m%Y") 
        paymentData["updated_at"] = datetime.now().strftime("%d%m%Y")

        result = self.collection.insert_one(paymentData)

        return {"statusCode": 201, "paymentId": str(result.inserted_id)}
      
      except PaymentException as e:
            raise e 
      except Exception as e:
          raise PaymentException(500, f"Error creating payment: {str(e)}")
      
    
    def getPaymentByUserId(self, userId: str):
        try:
            payment = self.collection.find_one({"userId": userId})

            if payment is None:
                raise PaymentException(404, "Payment not found.")

            paymentData = {
                "userId" : payment["userId"],
                "fullName" : payment["fullName"],
                "paymentType" : payment["paymentType"],
                "creditCardNumber" : payment["creditCardNumber"],
                "expiredMonth" : str(payment["expiredMonth"]),
                "cvv" : payment["cvv"]
            }

            return {"statusCode": 200, "payment": paymentData}

        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error fetching payment by ID: {str(e)}")
