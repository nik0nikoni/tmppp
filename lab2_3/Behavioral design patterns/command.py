from abc import ABC, abstractmethod


# 1. Интерфейс команды
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# 2. Receiver (исполнитель)
class Light:
    def turn_on(self):
        return "Свет включен"

    def turn_off(self):
        return "Свет выключен"


# 3. Конкретные команды
class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        return self.light.turn_on()


class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        return self.light.turn_off()


# 4. Invoker (вызывающий)
class RemoteControl:
    def __init__(self, command: Command):
        self.command = command

    def press_button(self):
        return self.command.execute()


# Использование
light = Light()

on_command = TurnOnCommand(light)
off_command = TurnOffCommand(light)

remote = RemoteControl(on_command)
print(remote.press_button())

remote.command = off_command
print(remote.press_button())