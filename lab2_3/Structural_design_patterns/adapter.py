from abc import ABC, abstractmethod


# 1. Интерфейс, который ожидает наша система
class DataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass


# 2. Чужой класс (мы его не можем изменить)
class ExternalAPI:
    def fetch_data(self):
        return "Данные из внешнего API"


# 3. Adapter
class APIAdapter(DataSource):
    def __init__(self, external_api: ExternalAPI):
        self.external_api = external_api

    def get_data(self):
        # "переводим" вызов
        return self.external_api.fetch_data()


# Использование

api = ExternalAPI()
data_source = APIAdapter(api)

print(data_source.get_data())