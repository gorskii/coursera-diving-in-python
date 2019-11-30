"""Часто при зачислении каких-то средств на счет с нас берут комиссию.
Давайте реализуем похожий механизм с помощью дескрипторов. Напишите
дескриптор Value, который будет использоваться в нашем классе Account. """


class Value(object):
    """Descriptor class for Account values"""
    pass


class Account(object):
    """У аккаунта будет атрибут commission. Именно эту коммиссию и нужно
    вычитать при присваивании значений в amount. """
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


new_account = Account(0.1)
new_account.amount = 100

print(new_account.amount)
