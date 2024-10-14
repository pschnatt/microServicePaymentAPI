import re

class Validator:

      @staticmethod
      def validatePositivePaymentAmount(payment_amount: int) -> bool:
            # Validate that payment amount is a positive integer
            return payment_amount > 0

      

 
      # @staticmethod
      # def validateCapacity(capacity: int, min_limit: int) -> bool:
      #       return capacity >= min_limit

      # @staticmethod
      # def validateAccountNumber(account_number: str) -> bool:
      #       # Validate that the account number consists of digits only and is of valid length
      #       return account_number.isdigit() and len(account_number) in [10, 12]

      # @staticmethod
      # def validateAccountBalance(account_balance: int, account_limit: int) -> bool:
      #       return 0 <= account_balance <= account_limit