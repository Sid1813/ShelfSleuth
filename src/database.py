# Create a persistent DuckDB database so our data can be queried using SQL by the future Text-to-SQL agent.

import duckdb

from pathlib import Path


# Create the processed-data directory if it does not already exist.

db_dir = Path("../data/processed")

db_dir.mkdir(parents=True, exist_ok=True)


# Create or open the ShelfSleuth DuckDB database.

db_path = db_dir / "shelfsleuth.duckdb"

con = duckdb.connect(str(db_path))