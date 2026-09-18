# Create a persistent DuckDB database so ShelfSleuth
# can query retail data using SQL.

import duckdb

from pathlib import Path


# Get the ShelfSleuth project root directory.

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Define the processed-data directory.

db_dir = PROJECT_ROOT / "data" / "processed"


# Create the directory if it does not already exist.

db_dir.mkdir(parents=True, exist_ok=True)


# Define the ShelfSleuth DuckDB database path.

db_path = db_dir / "shelfsleuth.duckdb"


# Open the DuckDB database.

con = duckdb.connect(str(db_path))