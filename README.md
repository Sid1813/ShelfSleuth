# ShelfSleuth 🔎

### AI-Powered Retail Inventory Investigation & Root-Cause Analysis

ShelfSleuth is an agentic AI system that turns natural-language retail questions into **data-backed investigations and actionable business recommendations**.

Instead of simply generating SQL or returning a number, ShelfSleuth follows an investigation workflow:

> **Question → SQL → Evidence → Business Context → Root Cause → Action → Critique**

The project combines a **semantic layer**, **business knowledge using the Open Knowledge Format (OKF)**, **Text-to-SQL**, deterministic database investigation, and specialized reasoning agents to investigate retail inventory and demand problems.

---

## 🧩 Problem

Retail analytics often involves more than answering questions such as:

- Which store has the lowest inventory?
- Which store has the highest average sales?
- Where is inventory coverage lowest?
- Which locations may have greater inventory risk?

A raw SQL query can identify *what happened*, but it does not necessarily explain:

- **Why** it happened
- **Whether** the result represents a potential business risk
- **What** should be investigated next
- **What action** an operations team could consider

ShelfSleuth is designed to bridge that gap by combining data analysis with business context and structured reasoning.

---

## 💡 What ShelfSleuth Does

A user can ask a question in natural language:

> **"Which store has the lowest average inventory?"**

ShelfSleuth then:

1. Understands the retail data model and business terminology.
2. Generates SQL to answer the question.
3. Executes the SQL against DuckDB.
4. Retrieves relevant business knowledge from the OKF bundle.
5. Runs a controlled investigation using predefined SQL analysis.
6. Uses the evidence and business context to identify potential root causes.
7. Generates practical business recommendations.
8. Critically reviews the reasoning and recommendations.

The result is not just a number, but an **evidence-backed business investigation**.

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │   User Question │
                         └────────┬────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │  Text-to-SQL Agent  │
                       │                     │
                       │ Question → SQL      │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │       DuckDB        │
                       │                     │
                       │ SQL → Data Evidence │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             ┌───────────────┐        ┌─────────────────────┐
             │ Semantic Layer│        │   Knowledge Agent   │
             │               │        │                     │
             │ Metrics       │        │     OKF Provider     │
             │ Dimensions    │        │                     │
             │ Business rules│        │ Business knowledge  │
             └───────┬───────┘        └──────────┬──────────┘
                     │                           │
                     └─────────────┬─────────────┘
                                   ▼
                       ┌─────────────────────┐
                       │   Root Cause Agent  │
                       │                     │
                       │ Evidence → Why      │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Action Planner Agent│
                       │                     │
                       │ Insight → Action    │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │    Critic Agent     │
                       │                     │
                       │ Validate reasoning  │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Final Investigation │
                       └─────────────────────┘

```

## 🔄 Workflow

### 1. User Question

The process starts with a natural-language business question.

For example:

> **"Which store has the lowest average inventory?"**

The user does not need to know SQL or the underlying database structure.

### 2. Text-to-SQL Agent

The **Text-to-SQL Agent** translates the natural-language question into executable SQL.

It uses the **semantic layer** to understand:

- Which metrics are available
- Which dimensions can be queried
- How important business metrics should be calculated
- Which database columns correspond to business concepts

The agent also includes retry and SQL-error correction logic.

### 3. DuckDB

The generated SQL is executed against a local **DuckDB** database containing the retail inventory data.

The database provides the factual evidence used by the downstream investigation.

The separation is intentional:

> **SQL → Database → Evidence**

This keeps factual data retrieval separate from LLM-generated interpretation.

### 4. Investigation Tool

ShelfSleuth also contains controlled investigation queries for deeper analysis.

For example, the current investigation layer can compare stores using:

- Average inventory
- Average units sold
- Average demand forecast
- Average inventory coverage

These investigations are deterministic SQL operations rather than arbitrary LLM-generated analysis.

### 5. Semantic Layer

The **Semantic Layer** provides structured information about the business meaning of the data.

The current implementation defines:

- **Metrics**
- **Dimensions**
- **Business rules**

Examples include:

- Average inventory
- Units sold
- Demand forecast
- Inventory coverage
- Store
- Product
- Category
- Region
- Date
- Seasonality
- Low inventory coverage

In simple terms:

> **Semantic Layer = What does the data mean?**

### 6. Knowledge Agent / OKF

The **Knowledge Agent** provides access to business knowledge stored using the **Open Knowledge Format (OKF)**.

The current OKF bundle contains business-rule concepts covering:

- **Inventory**
- **Demand**
- **Store Performance**

The OKF documents provide business context such as:

- Inventory should be evaluated relative to expected demand.
- Inventory coverage below one day can indicate a potential inventory-risk situation.
- A persistent gap between forecasted demand and actual sales may indicate forecast bias.
- Store-level inventory should be considered alongside sales and demand.

The Knowledge Agent is intentionally deterministic rather than being another LLM reasoning layer.

In simple terms:

> **OKF = What does the business know?**
>
> **Knowledge Agent = How does the pipeline access that knowledge?**

This keeps business knowledge separate from raw data and model-generated reasoning.

### 7. Root Cause Agent

The **Root Cause Agent** goes beyond the initial SQL answer.

It receives:

- The user's original question
- The initial SQL result
- Controlled investigation results
- Relevant OKF business knowledge

It then distinguishes between:

- **Direct evidence from the data**
- **Business interpretation**
- **Hypotheses requiring further investigation**

For example, a store may have the lowest absolute inventory without necessarily having the lowest inventory coverage.

This creates an important distinction between:

> **"Lowest inventory"**

and

> **"Potentially greater inventory risk."**

The agent is explicitly instructed not to treat business rules as evidence from the database and not to claim causation without supporting evidence.

### 8. Action Planner Agent

The **Action Planner Agent** converts the investigation into practical recommendations.

For each recommendation, it identifies:

1. The proposed action
2. Why the action is appropriate
3. The business persona that should own it
4. The metric that should be monitored afterward

The goal is to move from:

> **Insight → Action**

rather than stopping at analysis.

### 9. Critic Agent

The **Critic Agent** provides a final validation layer.

It reviews the root-cause analysis and action plan for:

- Claims unsupported by the evidence
- Unsupported assumptions or causal claims
- Recommendations that do not logically follow from the analysis
- Missing caveats
- Unclear business ownership

In simple terms:

> **Critic = Does the final investigation actually make sense?**

---

## 🧠 Why Multiple Agents?

ShelfSleuth uses multiple specialized components because each stage has a different responsibility and potential failure mode.

| Component | Purpose |
|---|---|
| **Text-to-SQL Agent** | Translate business questions into executable SQL |
| **Investigation Tool** | Execute controlled SQL investigations |
| **Knowledge Agent** | Provide access to business knowledge / OKF |
| **Root Cause Agent** | Interpret evidence and identify potential causes |
| **Action Planner Agent** | Convert findings into operational recommendations |
| **Critic Agent** | Validate reasoning and recommendations |

The goal is not to create as many agents as possible.

Instead, the architecture separates the major stages of an investigation so that **data retrieval, business context, reasoning, action planning, and validation are not all handled by a single prompt**.

---

## 🔗 How the Key Concepts Fit Together

ShelfSleuth demonstrates how three important concepts work together in an AI analytics workflow.

### Semantic Layer

Provides structured knowledge about the **data model**.

> **"What does this metric, dimension, or business rule mean?"**

### OKF / Business Knowledge

Provides knowledge about the **business context**.

> **"What business rules should influence how the data is interpreted?"**

### Text-to-SQL

Connects the **user's question to the database**.

> **"How do I query the database to answer this question?"**

Together:

> **User Question → Semantic Understanding → SQL → Evidence → Business Knowledge → Reasoning → Action**

---

## 🔍 Example Investigation

### Question

> **"Which store has the lowest average inventory?"**

### Initial SQL Result

ShelfSleuth identifies:

> **S004 — Average Inventory: ~272.30**

The investigation does not stop at this result.

The controlled investigation compares store-level inventory, sales, demand forecast, and inventory coverage.

The Root Cause Agent then uses these results together with relevant OKF business rules.

The analysis can distinguish between:

- The store with the lowest absolute inventory
- The store with lower inventory coverage
- Potential explanations that require additional investigation

The Action Planner then converts supported findings into recommended actions, while the Critic Agent reviews the reasoning before the final investigation is returned.

This illustrates the main idea behind ShelfSleuth:

> **The answer to the question is not necessarily the same as the underlying business problem.**

---

## 📊 Evaluation & Robustness

ShelfSleuth has been tested using deterministic DuckDB queries and representative retail business questions.

The complete investigation pipeline was successfully executed for:

> **"Which store has the lowest average inventory?"**

The generated SQL executed successfully against DuckDB, the relevant OKF concepts were retrieved, the controlled investigation completed, and the downstream Root Cause, Action Planner, and Critic stages executed successfully.

During development, additional live evaluations were also attempted. Some runs were interrupted by Gemini API availability and free-tier quota limitations. These are treated as **evaluation-environment limitations**, rather than failures of the underlying ShelfSleuth architecture.

The evaluation setup can be extended with additional API capacity or mocked/cached LLM responses for larger-scale testing.

---

## 📁 Project Structure

```text
ShelfSleuth/
│
├── agents/
│   ├── text_to_sql_agent.py
│   ├── knowledge_agent.py
│   ├── root_cause_agent.py
│   ├── action_planner_agent.py
│   ├── critic_agent.py
│   └── research_pipeline.py
│
├── data/
│   └── processed/
│
├── notebooks/
│   └── 01_data_reconnaissance.ipynb
│
├── okf/
│   ├── index.md
│   ├── log.md
│   ├── inventory.md
│   ├── demand.md
│   ├── store-performance.md
│   ├── loader.py
│   └── __init__.py
│
├── semantic_layer/
│   └── metrics.py
│
├── src/
│   └── database.py
│
├── tools/
│   ├── investigation_tool.py
│   └── sql_tool.py
│
├── requirements.txt
└── README.md

```

## 🛠️ Tech Stack

- **Python** — core implementation
- **DuckDB** — analytical database
- **SQL** — deterministic data investigation
- **Google Gemini** — LLM for Text-to-SQL and reasoning
- **Open Knowledge Format (OKF)** — structured business knowledge
- **PyYAML** — parsing OKF YAML frontmatter
- **VS Code** — development and experimentation

---

## 🎯 Purpose

This project was created as a hands-on exercise to understand how **Open Knowledge Format (OKF), semantic layers, Text-to-SQL, and agentic reasoning** can work together in an AI-powered analytics workflow.

The project emphasizes a separation between:

> **Data → Business Knowledge → Reasoning → Action**

This makes it possible to investigate not only *what happened*, but also how business context can be used to interpret the result and determine what should be investigated next.

---

# 👨‍💻 Author

**Siddharth Ranganatha**
