# 1. Подсистема: курсы
class CourseService:
    def create_course(self, title):
        return f"Курс '{title}' создан."


# 2. Подсистема: тесты
class TestService:
    def create_test(self, course_title):
        return f"Тест для курса '{course_title}' создан."


# 3. Подсистема: сертификаты
class CertificateService:
    def prepare_certificate(self, course_title):
        return f"Сертификат для курса '{course_title}' подготовлен."


# 4. Facade / Фасад
class CourseCreationFacade:
    def __init__(self):
        self.course_service = CourseService()
        self.test_service = TestService()
        self.certificate_service = CertificateService()

    def create_full_course(self, title):
        result = []

        result.append(self.course_service.create_course(title))
        result.append(self.test_service.create_test(title))
        result.append(self.certificate_service.prepare_certificate(title))

        return "\n".join(result)


# Использование
facade = CourseCreationFacade()

print(facade.create_full_course("Python Basics"))