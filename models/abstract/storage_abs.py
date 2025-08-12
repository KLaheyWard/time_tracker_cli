from abc import ABC, abstractmethod


class StorageAbs(ABC):
    @abstractmethod
    def add(new_entry):
        raise NotImplementedError("Must implement StorageAbs.add()")

    @abstractmethod
    def update(id, new_entry):
        raise NotImplementedError("Must implement StorageAbs.update()")

    @abstractmethod
    def delete(id):
        raise NotImplementedError("Must implement StorageAbs.delete()")

    @abstractmethod
    def get(id):
        raise NotImplementedError("Must implement StorageAbs.get()")

    @abstractmethod
    def get_all(id):
        raise NotImplementedError("Must implement StorageAbs.get_all()")