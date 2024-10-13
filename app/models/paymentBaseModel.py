from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class paymentType(str, Enum):
    american = "American"
    # italian = "Italian"
    # chinese = "Chinese"
    # mexican = "Mexican"
    # indian = "Indian"
    # french = "French"
    # japanese = "Japanese"
    # mediterranean = "Mediterranean"
    # thai = "Thai"
    # spanish = "Spanish"
    # greek = "Greek"
    # vietnamese = "Vietnamese"
    # korean = "Korean"
    # caribbean = "Caribbean"
    # middle_eastern = "Middle Eastern"

class paymentInfo(BaseModel):
  phoneNumber : str
  email : Optional[str]

class OperatingHour(BaseModel):
  openTime : datetime
  closeTime : datetime

class PaymentMutation(BaseModel):
  restaurantName : str
  # location : str
  # type : paymentType
  # contactInfo : pyamentInfo
  # operatingHour : OperatingHour
  # capacity : int
  # description : Optional[str]
  # cost : int
