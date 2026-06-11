class Observer:
    def update(self, message: str):
        raise NotImplementedError("Method update() must be implemented in subclasses")


class EmailNotifier(Observer):
    def update(self, message: str):
        print(f"[EMAIL NOTIFICATION] {message}")


class SmsNotifier(Observer):
    def update(self, message: str):
        print(f"[SMS NOTIFICATION] {message}")


class SystemNotifier(Observer):
    def update(self, message: str):
        print(f"[SYSTEM NOTIFICATION] {message}")


class NotificationCenter:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)


class DatabaseNotifier(Observer):
    def __init__(self, repository, user_id: int | None = None, channel: str = "system"):
        self.repository = repository
        self.user_id = user_id
        self.channel = channel

    def update(self, message: str):
        self.repository.create(self.user_id, self.channel, message)
