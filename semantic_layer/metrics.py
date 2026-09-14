# Define the business meaning of important metrics so the AI can use consistent definitions.

METRICS = {
    "average_inventory": {
        "description": "Average inventory level across observations",
        "expression": 'AVG("Inventory Level")',
    },

    "units_sold": {
        "description": "Total number of units sold",
        "expression": 'SUM("Units Sold")',
    },

    "demand_forecast": {
        "description": "Total forecasted demand",
        "expression": 'SUM("Demand Forecast")',
    },

    "inventory_coverage": {
        "description": "Inventory available relative to forecasted demand",
        "expression": 'AVG("Inventory Level" / NULLIF("Demand Forecast", 0))',
    },
}

# Define the dimensions that can be used to group or filter our metrics.

DIMENSIONS = {
    "store": '"Store ID"',
    "product": '"Product ID"',
    "category": '"Category"',
    "region": '"Region"',
    "date": '"Date"',
    "seasonality": '"Seasonality"',
}

# Define a simple business rule for identifying observations with less than one day of forecast-based inventory coverage.

BUSINESS_RULES = {
    "low_inventory_coverage": {
        "description": "Inventory is less than one day of forecasted demand",
        "condition": '"Inventory Level" < "Demand Forecast"',
    },
}

# Combine our metrics, dimensions, and business rules into a compact description
# that can later be provided to the Text-to-SQL agent.

def get_semantic_context():
    return {
        "metrics": METRICS,
        "dimensions": DIMENSIONS,
        "business_rules": BUSINESS_RULES,
    }