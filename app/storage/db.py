from abc import ABC, abstractmethod

class Db(ABC):

    def __init__(self, f):
        self.db_file = f

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
    def update(self, entry):
        pass
