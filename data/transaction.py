class Transaction():
    def __init__(self, id, amount, date):
        self.__id = id
        self.__amount = amount
        self.__date = date

    def to_dict(self):
        return {
            "id": self.__id,
            "amount": self.__amount,
            "date": self.__date,
        }