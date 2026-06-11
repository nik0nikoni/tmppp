from abc import ABC, abstractmethod


# 1. Интерфейс наблюдателя
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


# 2. Subject (издатель)
class Course:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


# 3. Конкретный наблюдатель
class Student(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} получил уведомление: {message}")



course = Course()

student1 = Student("Andrei")
student2 = Student("Maria")

course.subscribe(student1)
course.subscribe(student2)

course.notify("Новый урок доступен!")