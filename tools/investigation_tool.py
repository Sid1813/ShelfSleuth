# Define reusable SQL investigation patterns so agents can perform controlled data analysis


class InvestigationTool:

    def __init__(self, database_connection):

        # Store the DuckDB connection used to execute investigation queries

        self.con = database_connection


    # Compare inventory, sales, and forecast across stores

    def store_inventory_comparison(self):

        # Execute a controlled query that provides evidence about store-level inventory

        query = """
        SELECT
            "Store ID",
            AVG("Inventory Level") AS avg_inventory,
            AVG("Units Sold") AS avg_units_sold,
            AVG("Demand Forecast") AS avg_demand_forecast,
            AVG(
                "Inventory Level" / NULLIF("Demand Forecast", 0)
            ) AS avg_inventory_coverage
        FROM retail_inventory
        GROUP BY "Store ID"
        ORDER BY avg_inventory ASC
        """


        # Execute the investigation query and return the result

        return self.con.execute(query).fetchdf()