from abc import ABC, abstractmethod


class StoreAbs(ABC):
    @abstractmethod
    def add_entry(self, *args, **kwargs) -> None:
        """Prepares an entry for it to be saved somewhere."""
        raise NotImplementedError

    @abstractmethod
    def update_entry(self, id) -> None:
        """Updates an existing entry in the storage."""
        raise NotImplementedError

    @abstractmethod
    def delete_entry(self, id) -> None:
        """Deletes an existing entry in the storage."""
        raise NotImplementedError

    @abstractmethod
    def get_entry(self, id) -> None:
        """Gets the entry with corresponding id."""
        raise NotImplementedError

    @abstractmethod
    def get_all_entries(self) -> None:
        """Gets all of the entries."""
        raise NotImplementedError