from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class PaymentMutation(BaseModel):
  fullName : str
  paymentType : str
  creditCardNumber : str
  expiredMonth : datetime
  cvv: str
