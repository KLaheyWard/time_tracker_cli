from abc import ABC, abstractmethod


class SingleValueStorageAbs(ABC):
    @abstractmethod
    def get():
        raise NotImplementedError("Must implement SingleValueStorageAbs.get()")

    @abstractmethod
    def update(new_value):
        raise NotImplementedError(
            "Must implement SingleValueStorageAbs.update()")