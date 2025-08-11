from abc import ABC, abstractmethod


class SingleValueStoreAbs(ABC):
    @abstractmethod
    def get():
        raise NotImplementedError("Must implement SingleValueStoreAbs.get()")

    @abstractmethod
    def update(new_value):
        raise NotImplementedError(
            "Must implement SingleValueStoreAbs.update()")
