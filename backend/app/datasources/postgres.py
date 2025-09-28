from typing import Any, Iterable

from sqlalchemy import create_engine, text

from .base import BaseDataSource


class PostgresDataSource(BaseDataSource):
    name = "postgres"

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        if "dsn" not in config:
            raise ValueError("Postgres datasource requires 'dsn' in config")
        self.engine = create_engine(config["dsn"], pool_pre_ping=True, future=True)

    def run_sql(self, sql: str) -> Iterable[dict[str, Any]]:
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = [dict(row._mapping) for row in result]
        return rows

    def describe(self) -> str:
        return "PostgreSQL database"
