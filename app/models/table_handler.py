from abc import ABC, abstractmethod


class TableHandler:

    """Docstring for TableHandler. """

    @abstractmethod
    def insert(entry):
        """TODO: Docstring for insert.

        :entry: TODO
        :returns: TODO

        """
        pass

    @abstractmethod
    def delete(entry_id):
        """TODO: Docstring for delete.

        :entry_id: TODO
        :returns: TODO

        """
        pass

    @staticmethod
    @abstractmethod
    def update(entry_id, key, value):
        """TODO: Docstring for update.

        :entry_id: TODO
        :key: TODO
        :value: TODO
        :returns: TODO

        """
        pass

    @staticmethod
    @abstractmethod
    def get_all():
        """TODO: Docstring for get_all.
        :returns: TODO

        """
        pass

    @staticmethod
    @abstractmethod
    def get(entry_id):
        """TODO: Docstring for get.

        :entry_id: TODO
        :returns: TODO

        """
        pass
