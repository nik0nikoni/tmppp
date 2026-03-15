from abc import ABC, abstractmethod


# Product
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.gpu = None
        self.ssd = None
        self.os = None

    def show(self):
        print("Конфигурация компьютера:")
        print(f"CPU: {self.cpu}")
        print(f"RAM: {self.ram}")
        print(f"GPU: {self.gpu}")
        print(f"SSD: {self.ssd}")
        print(f"OS: {self.os}")


# Builder
class ComputerBuilder(ABC):
    @abstractmethod
    def set_cpu(self):
        pass

    @abstractmethod
    def set_ram(self):
        pass

    @abstractmethod
    def set_gpu(self):
        pass

    @abstractmethod
    def set_ssd(self):
        pass

    @abstractmethod
    def set_os(self):
        pass

    @abstractmethod
    def get_result(self):
        pass


# Concrete Builder
class GamingComputerBuilder(ComputerBuilder):
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self):
        self.computer.cpu = "Ryzen 7 7800X3D"

    def set_ram(self):
        self.computer.ram = "32 GB"

    def set_gpu(self):
        self.computer.gpu = "RTX 4070"

    def set_ssd(self):
        self.computer.ssd = "1 TB NVMe"

    def set_os(self):
        self.computer.os = "Windows 11"

    def get_result(self):
        return self.computer


# Director
class Director:
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder

    def build_gaming_pc(self):
        self.builder.set_cpu()
        self.builder.set_ram()
        self.builder.set_gpu()
        self.builder.set_ssd()
        self.builder.set_os()


# Client code
builder = GamingComputerBuilder()
director = Director(builder)

director.build_gaming_pc()
pc = builder.get_result()

pc.show()