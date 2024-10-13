from datetime import datetime
from bson import ObjectId
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

    
        paymentData["created_at"] = datetime.now().strftime("%d%m%Y") 
        paymentData["updated_at"] = datetime.now().strftime("%d%m%Y")
        

        result = self.collection.insert_one(paymentData)

        return {"statusCode": 201, "paymentId": str(result.inserted_id)}
      
      except PaymentException as e:
            raise e 
      except Exception as e:
          raise PaymentException(500, f"Error creating payment: {str(e)}")
      
    def getPaymentList(self):
      try:
        payments = list(self.collection.find({"status": 1}))

        paymentList = [{
            "paymentId": str(payment["_id"]),
            "paymentDate": payment["paymentDate"],
            "paymentAmount": payment["paymentAmount"],
            "paymentStatus": payment["paymentStatus"],
            "paymentMethod": payment["paymentMethod"],
            "paymentCurrency": payment["paymentCurrency"],
            "paymentType": payment["paymentType"],
            "paymentDescription": payment["paymentDescription"],

            "AccountID": payment["AccountID"],
            "AccountName": payment["AccountName"],
            "AccountType": payment["AccountType"],
            "AccountNumber": payment["AccountNumber"],
            "AccountBalance": payment["AccountBalance"],
            "AccountStatus": payment["AccountStatus"],
            "AccountCurrency": payment["AccountCurrency"],
            "AccountLimit": payment["AccountLimit"],

            "created_at": payment["created_at"],
            "updated_at": payment["updated_at"]   
        } for payment in payments]

        return {"statusCode": 200, "payments": paymentList}  
    
      except Exception as e:
        raise PaymentException(500, f"Error fetching payment list: {str(e)}")
    
    def getPaymentById(self, paymentId: str):
        try:
            payment = self.collection.find_one({"_id": ObjectId(paymentId), "status": 1})
            
            if payment is None:
                raise PaymentException(404, "payment not found.")
            
            paymentData = {
            
            "paymentId": str(payment["_id"]),
            "paymentDate": payment["paymentDate"],
            "paymentAmount": payment["paymentAmount"],
            "paymentStatus": payment["paymentStatus"],
            "paymentMethod": payment["paymentMethod"],
            "paymentCurrency": payment["paymentCurrency"],
            "paymentType": payment["paymentType"],
            "paymentDescription": payment["paymentDescription"],

            "AccountID": payment["AccountID"],
            "AccountName": payment["AccountName"],
            "AccountType": payment["AccountType"],
            "AccountNumber": payment["AccountNumber"],
            "AccountBalance": payment["AccountBalance"],
            "AccountStatus": payment["AccountStatus"],
            "AccountCurrency": payment["AccountCurrency"],
            "AccountLimit": payment["AccountLimit"],

            "created_at": payment["created_at"],
            "updated_at": payment["updated_at"]

            }
            return {"statusCode": 200, "restaurant": paymentData}
        
        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error fetching restaurant by ID: {str(e)}")
    
    def getAccountInPaymentFromSystemById(self, accountId: str):
        try:
            account = self.collection.find_one({"_id": ObjectId(accountId), "status": 1})
            
            if account is None:
                raise PaymentException(404, "Account not found.")
            
            accountData = {
            
            "AccountID": account["AccountID"],
            "AccountName": account["AccountName"],
            "AccountType": account["AccountType"],
            "AccountNumber": account["AccountNumber"],
            "AccountBalance": account["AccountBalance"],
            "AccountStatus": account["AccountStatus"],
            "AccountCurrency": account["AccountCurrency"],
            "AccountLimit": account["AccountLimit"],

            "created_at": account["created_at"],
            "updated_at": account["updated_at"]

            }
            return {"statusCode": 200, "account": accountData}
        
        except PaymentException as e:
            raise e
        except Exception as e:

            raise PaymentException(500, f"Error fetching account from system by ID: {str(e)}")
        
    def updatePayment(self, paymentMutation: PaymentMutation, paymentId: str, userId: str):
        try:
            paymentData = paymentMutation.model_dump()

            # if not (Validator.validateCapacity(len(restaurantData["restaurantName"]), 6)):
            #     raise PaymentException(400, "Restaurant name must be at least 6 characters long.")
            
            # if not Validator.validatePhoneNumber(restaurantData["contactInfo"]["phoneNumber"]):
            #     raise PaymentException(400, "Invalid phone number format.")
            
            # if restaurantData["contactInfo"]["email"] and not Validator.validateEmail(restaurantData["contactInfo"]["email"]):
            #     raise PaymentException(400, "Invalid email format.")

            # if restaurantData["operatingHour"]["openTime"] >= restaurantData["operatingHour"]["closeTime"]:
            #     raise PaymentException(400, "Open time must be earlier than close time.")
            
            existing_payment = self.collection.find_one({"_id": ObjectId(paymentId)})
            if not existing_payment:
                raise PaymentException(404, "payment not found.")
            
            updateData = {
                "$set": {
                    "paymentDate": paymentData["paymentDate"],
                    "paymentAmount": paymentData["paymentAmount"],
                    "paymentStatus": paymentData["paymentStatus"],
                    "paymentMethod": paymentData["paymentMethod"],
                    "paymentCurrency": paymentData["paymentCurrency"],
                    "paymentType": paymentData["paymentType"],
                    "paymentDescription": paymentData["paymentDescription"],
                    "AccountID": paymentData["AccountID"],
                    "AccountName": paymentData["AccountName"],
                    "AccountType": paymentData["AccountType"],
                    "AccountNumber": paymentData["AccountNumber"],
                    "AccountBalance": paymentData["AccountBalance"],
                    "AccountStatus": paymentData["AccountStatus"],
                    "AccountCurrency": paymentData["AccountCurrency"],
                    "AccountLimit": paymentData["AccountLimit"],
                    "updated_at": datetime.now().strftime("%d%m%Y")
                    
                }
            }

            result = self.collection.update_one({"_id": ObjectId(paymentId)}, updateData)

            return {"statusCode": 200, "paymentId": paymentId}

        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error updating payment: {str(e)}")
    
    def deletePayment(self, paymentId: str, userId: str):
      try:
          existing_payment = self.collection.find_one({"_id": ObjectId(paymentId)})
          if not existing_payment:
              raise PaymentException(404, "Restaurant not found.")
          
          updateData = {
              "$set": {
                  "status": 0,
                  "updated_by": userId,
                  "updated_when": datetime.now().strftime("%d%m%Y")
              }
          }
          result = self.collection.update_one({"_id": ObjectId(restaurantId)}, updateData)

          
          return {"statusCode": 200, "paymentId": paymentId}

      except PaymentException as e:
          raise e
      except Exception as e:
          raise PaymentException(500, f"Error updating payment: {str(e)}")

