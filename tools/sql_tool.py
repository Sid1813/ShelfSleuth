# Define a reusable SQL tool that allows agents to investigate data in DuckDB

class SQLTool:

    def __init__(self, database_connection):

        # Store the DuckDB connection so the tool can execute queries

        self.con = database_connection


    # Execute a read-only SQL query and return the result

    def run(self, sql):

        # Prevent the tool from modifying the database

        if not sql.strip().upper().startswith("SELECT"):

            raise ValueError("SQLTool only allows SELECT queries.")


        # Execute the query and return the results as a DataFrame

        return self.con.execute(sql).fetchdf()