from typing import Iterable

from .base import BaseDataSource


class StubDataSource(BaseDataSource):
    name = "stub"

    def run_sql(self, sql: str) -> Iterable[dict[str, object]]:
        return []

    def describe(self) -> str:
        return "Stub data source"


class BigQueryDataSource(StubDataSource):
    name = "bigquery"

    def describe(self) -> str:
        return "Google BigQuery dataset"


class HiveDataSource(StubDataSource):
    name = "hive"

    def describe(self) -> str:
        return "Hive SQL cluster"


class MySQLDataSource(StubDataSource):
    name = "mysql"

    def describe(self) -> str:
        return "MySQL database"
