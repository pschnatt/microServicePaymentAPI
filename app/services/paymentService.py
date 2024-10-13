from datetime import datetime
from bson import ObjectId
import certifi
from pymongo import MongoClient
from app.helpers.exception import PaymentException
from microServicePaymentAPI.app.models.paymentBaseModel import PaymentMutation
from app.core.config import settings
from app.helpers.validator import Validator

class PaymentService:
    def __init__(self):
      self.client = MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
      self.db = self.client[settings.DB_NAME]
      self.collection = self.db[settings.COLLECTION_NAME]

    def createPayment(self, paymentMutation : PaymentMutation, userId : str):
      try:
        restaurantData = paymentMutation.model_dump()

        if not (Validator.validateCapacity(len(restaurantData["restaurantName"]), 6)):
          raise PaymentException(400, "Restaurant name must be at least 6 characters long.")
        
        if not Validator.validatePhoneNumber(restaurantData["contactInfo"]["phoneNumber"]):
          raise PaymentException(400, "Invalid phone number format.")
                    
        if restaurantData["contactInfo"]["email"] and not Validator.validateEmail(restaurantData["contactInfo"]["email"]):
          raise PaymentException(400, "Invalid email format.")

        if restaurantData["operatingHour"]["openTime"] >= restaurantData["operatingHour"]["closeTime"]:
          raise PaymentException(400, "Open time must be earlier than close time.")
        
        restaurantData["created_by"] = userId
        restaurantData["created_when"] = datetime.now().strftime("%d%m%Y") 
        restaurantData["updated_by"] = userId 
        restaurantData["updated_when"] = datetime.now().strftime("%d%m%Y")
        restaurantData["status"] = 1
        result = self.collection.insert_one(restaurantData)

        return {"statusCode": 201, "restaurantId": str(result.inserted_id)}
      
      except PaymentException as e:
            raise e 
      except Exception as e:
          raise PaymentException(500, f"Error creating restaurant: {str(e)}")
      
    def getPaymentList(self):
      try:
        restaurants = list(self.collection.find({"status": 1}))
        restaurantList = [{
            "restaurantId": str(restaurant["_id"]),
            "restaurantName": restaurant["restaurantName"],
            "location": restaurant["location"],
            "type": restaurant["type"],
            "contactInfo": restaurant["contactInfo"],
            "operatingHour": str(restaurant["operatingHour"]),
            "capacity": restaurant["capacity"],
            "description": restaurant["description"],
            "cost" : restaurant["cost"],
            "createdBy": restaurant["created_by"],
            "createdWhen": restaurant["created_when"],
            "updatedBy": restaurant["updated_by"],
            "updatedWhen": restaurant["updated_when"]
        } for restaurant in restaurants]

        return {"statusCode": 200, "restaurants": restaurantList}  
    
      except Exception as e:
        raise PaymentException(500, f"Error fetching restaurant list: {str(e)}")
    
    def getPaymentById(self, restaurantId: str):
        try:
            restaurant = self.collection.find_one({"_id": ObjectId(restaurantId), "status": 1})
            
            if restaurant is None:
                raise PaymentException(404, "Restaurant not found.")
            
            restaurantData = {
                "restaurantId": str(restaurant["_id"]),
                "restaurantName": restaurant["restaurantName"],
                "location": restaurant["location"],
                "type": restaurant["type"],
                "contactInfo": restaurant["contactInfo"],
                "operatingHour": str(restaurant["operatingHour"]),
                "capacity": restaurant["capacity"],
                "description": restaurant["description"],
                "cost" : restaurant["cost"],
                "createdBy": restaurant["created_by"],
                "createdWhen": restaurant["created_when"],
                "updatedBy": restaurant["updated_by"],
                "updatedWhen": restaurant["updated_when"]
            }
            return {"statusCode": 200, "restaurant": restaurantData}
        
        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error fetching restaurant by ID: {str(e)}")
    
    def updatePayment(self, paymentMutation: PaymentMutation, restaurantId: str, userId: str):
        try:
            restaurantData = paymentMutation.model_dump()

            if not (Validator.validateCapacity(len(restaurantData["restaurantName"]), 6)):
                raise PaymentException(400, "Restaurant name must be at least 6 characters long.")
            
            if not Validator.validatePhoneNumber(restaurantData["contactInfo"]["phoneNumber"]):
                raise PaymentException(400, "Invalid phone number format.")
            
            if restaurantData["contactInfo"]["email"] and not Validator.validateEmail(restaurantData["contactInfo"]["email"]):
                raise PaymentException(400, "Invalid email format.")

            if restaurantData["operatingHour"]["openTime"] >= restaurantData["operatingHour"]["closeTime"]:
                raise PaymentException(400, "Open time must be earlier than close time.")
            
            existing_restaurant = self.collection.find_one({"_id": ObjectId(restaurantId)})
            if not existing_restaurant:
                raise PaymentException(404, "Restaurant not found.")
            if existing_restaurant["status"] == 0:
                raise PaymentException(400, "Cannot update restaurant because it is inactive.")

            updateData = {
                "$set": {
                    "restaurantName": restaurantData["restaurantName"],
                    "location": restaurantData["location"],
                    "type": restaurantData["type"],
                    "contactInfo": restaurantData["contactInfo"],
                    "operatingHour": restaurantData["operatingHour"],
                    "capacity": restaurantData["capacity"],
                    "description": restaurantData["description"],
                    "cost" : restaurantData["cost"],
                    "updated_by" : userId,
                    "updated_When": datetime.now().strftime("%d%m%Y") 
                }
            }

            result = self.collection.update_one({"_id": ObjectId(restaurantId)}, updateData)

            return {"statusCode": 200, "restaurantId": restaurantId}

        except PaymentException as e:
            raise e
        except Exception as e:
            raise PaymentException(500, f"Error updating restaurant: {str(e)}")
    
    def deletePayment(self, restaurantId: str, userId: str):
      try:
          existing_restaurant = self.collection.find_one({"_id": ObjectId(restaurantId)})
          if not existing_restaurant:
              raise PaymentException(404, "Restaurant not found.")
          if existing_restaurant["status"] == 0:
              raise PaymentException(400, "Restaurant is already inactive.")
          updateData = {
              "$set": {
                  "status": 0,
                  "updated_by": userId,
                  "updated_when": datetime.now().strftime("%d%m%Y")
              }
          }
          result = self.collection.update_one({"_id": ObjectId(restaurantId)}, updateData)

          if result.modified_count == 0:
              raise PaymentException(500, "Error updating restaurant status.")
          return {"statusCode": 200, "restaurantId": restaurantId}

      except PaymentException as e:
          raise e
      except Exception as e:
          raise PaymentException(500, f"Error updating restaurant status: {str(e)}")


    def checkAvailability():
       pass

    
