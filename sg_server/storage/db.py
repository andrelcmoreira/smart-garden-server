from abc import ABC, abstractmethod

class Db(ABC):

    @abstractmethod
    def add(self, entry):
        pass

    @abstractmethod
    def rm(self, entry):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, id, param, value):
        pass
