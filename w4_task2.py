""" Часто при зачислении каких-то средств на счет с нас берут комиссию.
    Давайте реализуем похожий механизм с помощью дескрипторов. Напишите
    дескриптор Value, который будет использоваться в нашем классе Account.
"""


class Value:
    """ A data descriptor that gets Account's _amount field or subtracts
        commission from it while sets it's value.
        Probably not the best way to implement such behavior - it is not good to
        access a protected variable '_amount'.
    """

    def __get__(self, obj, obj_type=None):
        return obj._amount

    def __set__(self, obj, value: float):
        print(f'Updating amount by {value}')
        obj._amount = value - value * obj.commission


class Account:
    """ У аккаунта будет атрибут commission. Именно эту коммиссию и нужно
        вычитать при присваивании значений в amount.
    """

    amount = Value()  # A property-like descriptor

    def __init__(self, commission=0.0):
        self.commission = commission
        self._amount = 0.0


def main():
    """Initializing some instances of Account class, testing Value descriptor"""

    new_account = Account(commission=0.1)
    new_account.amount = 100
    print(f"1st account amount is '{new_account.amount}'")

    another_account = Account(commission=0.2)
    another_account.amount = 150
    print(f"2nd account amount is '{another_account.amount}'")
    print(f"1st account amount is still '{new_account.amount}'")


if __name__ == '__main__':
    main()
