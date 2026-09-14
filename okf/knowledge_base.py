# Define business knowledge that the AI can use alongside quantitative SQL results

KNOWLEDGE_BASE = {

    "inventory": [
        "Low inventory can increase the risk of stockouts.",

        "Inventory should be evaluated relative to expected demand, not only as an absolute quantity.",

        "Inventory coverage below one day indicates a potential inventory-risk situation.",
    ],


    "demand": [
        "Demand Forecast represents expected demand for the observation.",

        "A persistent gap between forecasted demand and actual units sold may indicate forecast bias.",
    ],


    "store_performance": [
        "Store-level inventory differences should be investigated alongside sales and demand patterns.",

        "A store with low inventory is not necessarily underperforming if its demand is also low.",
    ],
}