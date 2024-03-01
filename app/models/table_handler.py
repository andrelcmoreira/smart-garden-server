from abc import ABC, abstractmethod


class TableHandler(ABC):

    '''
    Define a base sql table handler.

    '''

    @staticmethod
    @abstractmethod
    def insert(entry):
        '''
        Insert an entry into the table.

        :entry: Entry data.

        '''

    @staticmethod
    @abstractmethod
    def delete(entry_id):
        '''
        Delete a record from the table.

        :entry_id: Record ID.

        '''

    @staticmethod
    @abstractmethod
    def update(entry_id, key, value):
        '''
        Update a table's record.

        :entry_id: Record ID.
        :key: Column to be updated.
        :value: New value to replace the old one.

        '''

    @staticmethod
    @abstractmethod
    def get_all():
        '''
        Get all elements from the table.

        :returns: All the table entries.

        '''

    @staticmethod
    @abstractmethod
    def get(entry_id):
        '''
        Get an specific element from the table.

        :entry_id: ID of entry.
        :returns: The entry data.

        '''

    @staticmethod
    @abstractmethod
    def entry_exists(entry_id):
        '''
        Verify if an entry specified by 'entry_id' exists on the table.

        :entry_id: ID of entry.
        :returns: True if it exist; otherwise False.

        '''
