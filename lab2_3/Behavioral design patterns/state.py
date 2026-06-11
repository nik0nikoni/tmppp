from abc import ABC, abstractmethod


# 1. Интерфейс состояния
class OrderState(ABC):
    @abstractmethod
    def next_state(self, order):
        pass

    @abstractmethod
    def get_status(self):
        pass


# 2. Конкретные состояния
class CreatedState(OrderState):
    def next_state(self, order):
        order.state = PaidState()

    def get_status(self):
        return "Заказ создан"


class PaidState(OrderState):
    def next_state(self, order):
        order.state = ShippedState()

    def get_status(self):
        return "Заказ оплачен"


class ShippedState(OrderState):
    def next_state(self, order):
        print("Заказ уже отправлен")

    def get_status(self):
        return "Заказ отправлен"


# 3. Контекст
class Order:
    def __init__(self):
        self.state = CreatedState()

    def next(self):
        self.state.next_state(self)

    def status(self):
        return self.state.get_status()


# Использование
order = Order()

print(order.status())

order.next()
print(order.status())

order.next()
print(order.status())