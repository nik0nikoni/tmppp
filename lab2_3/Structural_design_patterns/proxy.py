from abc import ABC, abstractmethod


# 1. Общий интерфейс
class Certificate(ABC):
    @abstractmethod
    def download(self):
        pass


# 2. Реальный объект
class RealCertificate(Certificate):
    def __init__(self, username, course_title):
        self.username = username
        self.course_title = course_title

    def download(self):
        return f"Сертификат пользователя {self.username} по курсу '{self.course_title}' скачан."


# 3. Proxy / Заместитель
class CertificateProxy(Certificate):
    def __init__(self, username, course_title, course_completed):
        self.username = username
        self.course_title = course_title
        self.course_completed = course_completed

        # Реальный объект пока не создаём
        self.real_certificate = None

    def download(self):
        if not self.course_completed:
            return "Доступ запрещён: курс ещё не пройден."

        # Создаём реальный объект только при необходимости
        if self.real_certificate is None:
            self.real_certificate = RealCertificate(
                self.username,
                self.course_title
            )

        return self.real_certificate.download()


# Пример 1: курс не пройден
certificate1 = CertificateProxy(
    username="Andrei",
    course_title="Python Basics",
    course_completed=False
)

print(certificate1.download())


# Пример 2: курс пройден
certificate2 = CertificateProxy(
    username="Maria",
    course_title="Python Basics",
    course_completed=True
)

print(certificate2.download())