from abc import ABC, abstractmethod
class Generator(ABC):
    @abstractmethod
    def get_instance():
        pass

    @abstractmethod
    def generate_sync():
        pass

    @abstractmethod
    def generate_one():
        pass

    @abstractmethod
    def generate_many():
        pass