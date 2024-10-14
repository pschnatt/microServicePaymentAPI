import re

class Validator:

      @staticmethod
      def validatePositivePaymentAmount(payment_amount: int) -> bool:
            return payment_amount > 0