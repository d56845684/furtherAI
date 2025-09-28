from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseDataSource(ABC):
    name: str

    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def run_sql(self, sql: str) -> Iterable[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def describe(self) -> str:
        raise NotImplementedError
