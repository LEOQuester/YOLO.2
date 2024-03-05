from repo.FirebaseDriver import FirebaseDriver
from data.transaction import Transaction

class LedgerService:
    def __init__(self):
        self.__driver = FirebaseDriver()

    def save_to_db(self, transaction: Transaction):
        transaction_dict = transaction.to_dict()
        operation = self.__driver.create_document('transactions', transaction_dict)
        if operation:
            return {"success": True, "message": "Transaction Saved!"}
        return {"success": False, "message": "Error Occurred!"}