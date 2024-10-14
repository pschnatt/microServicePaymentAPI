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


        paymentData["created_by"] = userId
        paymentData["created_at"] = datetime.now().strftime("%d%m%Y") 
        paymentData["updated_at"] = datetime.now().strftime("%d%m%Y")
        
        if not (Validator.validatePositivePaymentAmount(paymentData["paymentAmount"])):
           raise PaymentException(400, "payment amount must not be less than 0")
        
        # if not (Validator.validateAmount(bookingData["costPerPerson"], 0)):
        #     raise BookingException(400, "cost must not be less than 1")
        
        # if bookingData["reservationDate"]["startFrom"] >= bookingData["reservationDate"]["to"]:
        #   raise BookingException(400, "'start' time must be earlier than 'to' time.")

        result = self.collection.insert_one(paymentData)

        return {"statusCode": 201, "paymentId": str(result.inserted_id)}
      
      except PaymentException as e:
            raise e 
      except Exception as e:
          raise PaymentException(500, f"Error creating payment: {str(e)}")
      
    def getPaymentList(self):
      try:
        
        payments = list(self.collection.find())
        print(payments)

        paymentList = [{
            "_id": str(payment["_id"]),
            "created_by": payment["created_by"],
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

            "created_at": str(payment["created_at"]),
            "updated_at": str(payment["updated_at"])   
        } for payment in payments]

        return {"statusCode": 200, "payments": paymentList}  
    
      except Exception as e:
        raise PaymentException(500, f"Error fetching payment list: {str(e)}")
    
    def getPaymentByPaymentId(self, paymentId: str):
        try:
            # Find the payment by paymentId in the collection
            payment = self.collection.find_one({"_id": ObjectId(paymentId)})

            # If no payment is found, raise a PaymentException
            if payment is None:
                raise PaymentException(404, "Payment not found.")

            # Structure the payment data as a dictionary
            paymentData = {
                "_id": str(payment["_id"]),
                "created_by": payment["created_by"],
                "paymentDate": payment["paymentDate"].isoformat(),
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

            # Return a success response with the payment data
            return {"statusCode": 200, "payment": paymentData}

        except PaymentException as e:
            # Re-raise the custom exception if it's a PaymentException
            raise e
        except Exception as e:
            # Raise a PaymentException for any other error
            raise PaymentException(500, f"Error fetching payment by ID: {str(e)}")
           
    def getAllPaymentsByUserId(self, userId: str):
        try:
            payments = list(self.collection.find({"created_by": userId}))

            paymentList = [{
                "_id": str(payment["_id"]),

                "created_by": payment["created_by"],
                "paymentDate": payment["paymentDate"].isoformat(),
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
        
        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error fetching payments by user ID: {str(e)}")

    def getAccountInPaymentFromSystemByPaymentId(self, paymentId: str):
        try:
            payment = self.collection.find_one({"_id": ObjectId(paymentId)})
            
            if payment is None:
                raise PaymentException(404, "Account not found.")
            
            accountData = {
            
            "AccountID": payment["AccountID"],
            "AccountName": payment["AccountName"],
            "AccountType": payment["AccountType"],
            "AccountNumber": payment["AccountNumber"],
            "AccountBalance": payment["AccountBalance"],
            "AccountStatus": payment["AccountStatus"],
            "AccountCurrency": payment["AccountCurrency"],
            "AccountLimit": payment["AccountLimit"]

            }
            return {"statusCode": 200, "account": accountData}
        
        except PaymentException as e:
            raise e
        except Exception as e:

            raise PaymentException(500, f"Error fetching account from system by ID: {str(e)}")
        
    def updatePayment(self, paymentMutation: PaymentMutation, paymentId: str):
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
                    "created_by": paymentData["created_by"],
                    "paymentDate": paymentData["paymentDate"].isoformat(),
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
    
          

    def deletePayment(self, userId: str, paymentId: str):
        try:
            payment = self.collection.find_one({"_id": ObjectId(paymentId)})

            if payment is None:
                raise PaymentException(404, "Payment not found.")
            
            if payment["created_by"] != userId:
                raise PaymentException(403, "You are not authorized to delete this payment.")
            
            self.collection.delete_one({"_id": ObjectId(paymentId)})

            return {"statusCode": 200, "message": "Payment deleted successfully."}
        
        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error deleting payment: {str(e)}")