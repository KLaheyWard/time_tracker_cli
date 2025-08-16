from abc import ABC, abstractmethod
class EntryAbs(ABC):
    
    @property
    @abstractmethod
    def id(self) -> str:
        raise NotImplementedError("EntryAbs implementation must have property id")
    
    @abstractmethod
    def fields() -> list[str]:
        raise NotImplementedError("fields() must be defined in implementation of EntryAbs")
    
    @abstractmethod
    def set_id(self, new_id):
        raise NotImplementedError("EntryAbs implementation must have set_id() implementation")
        