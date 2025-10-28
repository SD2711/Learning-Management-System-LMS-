from abc import ABC, abstractmethod


class Teachable(ABC):
    @abstractmethod
    def teach(self) -> str:
        pass


class Assessable(ABC):
    @abstractmethod
    def assess_progress(self) -> str:
        pass
