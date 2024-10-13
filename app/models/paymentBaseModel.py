from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum



class PaymentMutation(BaseModel):

  paymentID: str
  paymentDate: datetime
  paymentAmount: int
  paymentStatus: str
  paymentMethod: str
  paymentCurrency: str
  paymentType: str
  paymentDescription: str


  AccountID: str
  AccountName: str
  AccountType: str
  AccountNumber: str
  AccountBalance: int
  AccountStatus: str
  AccountCurrency: str
  AccountLimit: int

  created_at: datetime
  updated_at: datetime
  # location : str
  # type : paymentType
  # contactInfo : pyamentInfo
  # operatingHour : OperatingHour
  # capacity : int
  # description : Optional[str]
  # cost : int
