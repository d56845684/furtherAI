from collections.abc import Callable
from typing import Any

from .base import BaseDataSource
from .postgres import PostgresDataSource
from .stubs import BigQueryDataSource, HiveDataSource, MySQLDataSource


DATASOURCE_REGISTRY: dict[str, Callable[[dict[str, Any]], BaseDataSource]] = {
    PostgresDataSource.name: PostgresDataSource,
    BigQueryDataSource.name: BigQueryDataSource,
    HiveDataSource.name: HiveDataSource,
    MySQLDataSource.name: MySQLDataSource,
}


def create_datasource(name: str, config: dict[str, Any]) -> BaseDataSource:
    factory = DATASOURCE_REGISTRY.get(name.lower())
    if not factory:
        raise ValueError(f"Unsupported datasource: {name}")
    return factory(config)
