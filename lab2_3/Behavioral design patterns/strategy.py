from abc import ABC, abstractmethod

# Меняю поведение во время выполнения
# 1. Интерфейс стратегии
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


# 2. Конкретные стратегии
class CardPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Оплата {amount} картой"


class CashPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Оплата {amount} наличными"


# 3. Контекст
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def execute_payment(self, amount):
        return self.strategy.pay(amount)


# Использование
context = PaymentContext(CardPayment())
print(context.execute_payment(100))

context.strategy = CashPayment()
print(context.execute_payment(100))