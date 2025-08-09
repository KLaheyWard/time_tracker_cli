from abc import ABC, abstractmethod
from typing import Type, TypeVar

T = TypeVar("T")
class StorageAbs(ABC):
    @abstractmethod
    def add(new_entry):
        raise NotImplementedError("Must implement StorageAbs.add()")
    
    @abstractmethod
    def update( id, new_entry):
        raise NotImplementedError("Must implement StorageAbs.update()")
    
    @abstractmethod
    def delete(id):
        raise NotImplementedError("Must implement StorageAbs.delete()")