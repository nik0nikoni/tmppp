'''
Абстрактная фабрика — это паттерн, 
который позволяет создавать семейства связанных объектов через общий интерфейс фабрики. 
Конкретные фабрики создают конкретные реализации продуктов, 
при этом клиентский код не зависит от их конкретных классов.
'''

from abc import ABC, abstractmethod

#Абс продукты
class Button(ABC):
    @abstractmethod
    def paint(self):
        pass


class Checkbox(ABC):
    @abstractmethod
    def paint(self):
        pass


#конкр. продукты
class WindowsButton(Button):
    def paint(self):
        print("Windows button")


class MacButton(Button):
    def paint(self):
        print("Mac button")


class WindowsCheckbox(Checkbox):
    def paint(self):
        print("Windows checkbox")


class MacCheckbox(Checkbox):
    def paint(self):
        print("Mac checkbox")


#абс фабрика
class GUIFactory(ABC):

    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass


#конк фабрики
class WindowsFactory(GUIFactory):

    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()


class MacFactory(GUIFactory):

    def create_button(self):
        return MacButton()

    def create_checkbox(self):
        return MacCheckbox()
    


def client_code(factory: GUIFactory):

    button = factory.create_button()
    checkbox = factory.create_checkbox()

    button.paint()
    checkbox.paint()


factory = WindowsFactory()
client_code(factory)