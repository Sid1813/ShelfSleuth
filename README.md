# ShelfSleuth 🔎

### AI-Powered Retail Inventory Investigation & Root-Cause Analysis

ShelfSleuth is an agentic AI system that turns natural-language retail questions into **data-backed investigations and actionable business recommendations**.

Instead of simply generating SQL or returning a number, ShelfSleuth follows an investigation workflow:

> **Question → SQL → Evidence → Business Context → Root Cause → Action → Critique**

The project combines a **semantic layer**, **business knowledge (OKF)**, **Text-to-SQL**, deterministic database investigation, and specialized reasoning agents to investigate retail inventory and demand problems.

---

## 🧩 Problem

Retail analytics often involves more than answering questions such as:

- Which store has the lowest inventory?
- Which store has the highest average sales?
- Where is forecast accuracy weakest?
- Which locations have the greatest inventory risk?

A raw SQL query can identify *what happened*, but it does not necessarily explain:

- **Why** it happened
- **Whether** the result represents a genuine business risk
- **What** should be investigated next
- **What action** an operations team should take

ShelfSleuth is designed to bridge that gap by combining data analysis with business context and structured reasoning.

---

## 💡 What ShelfSleuth Does

A user can ask a question in natural language:

> **"Which store has the lowest average inventory?"**

ShelfSleuth then:

1. Understands the retail data model and business terminology.
2. Generates SQL to answer the question.
3. Executes the SQL against the database.
4. Retrieves the relevant business knowledge and operational rules.
5. Investigates the result against related metrics and stores.
6. Identifies potential root causes and business risks.
7. Generates actionable recommendations.
8. Critically reviews the investigation for consistency and unsupported conclusions.

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
                       │   Investigation     │
                       │       Tool          │
                       │                     │
                       │ SQL → DB Evidence   │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             ┌───────────────┐        ┌─────────────────────┐
             │ Semantic Layer│        │   Knowledge Agent   │
             │               │        │     (OKF Provider)  │
             │ Data meaning  │        │                     │
             │ Metrics       │        │ Business knowledge  │
             │ Relationships │        │ and business rules  │
             └───────┬───────┘        └──────────┬──────────┘
                     │                           │
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

- Which tables contain the required data
- What columns represent
- How metrics should be calculated
- Which business concepts map to database fields

The agent also includes retry/correction logic to handle SQL generation errors.

### 3. Investigation Tool

The **Investigation Tool** executes the generated SQL against the DuckDB database.

Its role is deliberately deterministic:

> **SQL → Database → Evidence**

This separates factual database retrieval from LLM reasoning and provides downstream agents with concrete numerical evidence.

### 4. Semantic Layer

The **Semantic Layer** provides structured information about the data model.

It describes:

- Tables
- Columns
- Metrics
- Relationships
- Business meanings
- Relevant calculations

Its purpose is to help the LLM understand the data correctly rather than relying only on raw column names.

In simple terms:

> **Semantic Layer = What does the data mean?**

### 5. Knowledge Agent / OKF

The **Knowledge Agent** is a lightweight business-knowledge provider.

It exposes the project's **OKF (Operational Knowledge Framework)**, which contains business rules and domain knowledge related to areas such as:

- Inventory coverage
- Stockout risk
- Forecast accuracy
- Forecast bias
- Replenishment
- Inventory thresholds
- Operational constraints

The Knowledge Agent is intentionally deterministic rather than being another LLM reasoning layer.

In simple terms:

> **OKF = What does the business know?**  
> **Knowledge Agent = How does the pipeline access that knowledge?**

This keeps business knowledge separate from raw data and model-generated reasoning.

### 6. Root Cause Agent

The **Root Cause Agent** goes beyond the initial SQL answer.

It examines the evidence and business context to investigate:

- What is unusual?
- Is the result actually risky?
- What other factors may explain it?
- Is the issue isolated or systemic?
- Which related metrics or entities should be considered?

For example, a store may have the lowest absolute inventory but still have healthy inventory coverage.

The agent therefore distinguishes between:

> **"Lowest inventory"**

and

> **"Highest business risk."**

This is a key difference between ShelfSleuth and a simple Text-to-SQL system.

### 7. Action Planner Agent

The **Action Planner Agent** converts the investigation into operational recommendations.

It focuses on:

- What should be done?
- Why should it be done?
- What should be investigated further?
- What metric should be monitored?

Possible recommendations include:

- Recalibrating a forecast where systematic bias is observed
- Monitoring a store with low inventory coverage
- Investigating replenishment or stockout patterns
- Reviewing inventory levels at a more granular level

The goal is to move from:

> **Insight → Action**

rather than stopping at analysis.

### 8. Critic Agent

The **Critic Agent** provides a final validation layer.

It reviews the investigation and checks whether:

- The reasoning is consistent with the evidence
- Recommendations are supported by the analysis
- Conclusions overreach the available data
- Important inconsistencies are present

In simple terms:

> **Critic = Does the final investigation actually make sense?**

---

## 🧠 Why Multiple Agents?

ShelfSleuth uses multiple specialized components because each stage has a different responsibility and potential failure mode.

| Component | Purpose |
|---|---|
| **Text-to-SQL Agent** | Translate business questions into executable SQL |
| **Investigation Tool** | Execute SQL and retrieve factual database evidence |
| **Knowledge Agent** | Provide access to business knowledge / OKF |
| **Root Cause Agent** | Investigate evidence and identify potential causes |
| **Action Planner Agent** | Convert findings into operational recommendations |
| **Critic Agent** | Validate reasoning and recommendations |

The goal is not to create as many agents as possible.

Instead, the architecture separates the major stages of an investigation so that **data retrieval, business context, reasoning, action planning, and validation are not all handled by a single prompt**.

---

## 🔗 How the Key Concepts Fit Together

ShelfSleuth demonstrates how three important concepts work together in an AI analytics workflow.

### Semantic Layer

Provides structured knowledge about the **data**.

> **"What does this table, column, or metric mean?"**

### OKF / Business Knowledge

Provides knowledge about the **business**.

> **"What does this metric mean operationally, and what rules or thresholds matter?"**

### Text-to-SQL

Connects the **user's question to the data**.

> **"How do I query the database to answer this question?"**

Together:

> **User Question → Semantic Understanding → SQL → Evidence → Business Knowledge → Reasoning → Action**

---

## 🔍 Example Investigation

### Question

> **"Which store has the lowest average inventory?"**

### SQL Result

ShelfSleuth identifies:

> **S004 — Average Inventory: ~272.30**

However, the investigation does not stop there.

The Root Cause Agent compares the result with other stores and related inventory metrics.

It identifies that:

- S004 has the lowest absolute average inventory.
- Its inventory coverage is not necessarily the most concerning.
- S002 has lower inventory coverage and may be more sensitive to demand fluctuations.
- Broader forecast behaviour may also contribute to inventory pressure.

The Action Planner then recommends actions such as:

- Investigating replenishment and stockout patterns for S004
- Monitoring S002 because of its lower coverage
- Reviewing forecast calibration where systematic bias is observed

The Critic Agent reviews the investigation before the final result is returned.

This illustrates the main idea behind ShelfSleuth:

> **The answer to the question is not always the same as the root business problem.**

---

## 📊 Evaluation & Robustness

ShelfSleuth was evaluated using deterministic DuckDB queries and a small set of representative retail business questions.

The end-to-end pipeline was successfully executed on a representative investigation question, and the generated SQL result matched the deterministic database result.

Additional live evaluations were attempted, but the Gemini API free-tier request quota was exhausted during testing. These cases are therefore treated as **unevaluated due to API limits**, rather than failures of the ShelfSleuth pipeline.

The evaluation setup can be extended with additional API capacity or a mocked/cached LLM layer for larger-scale testing.

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
├── api/
│
├── data/
│   └── processed/
│
├── notebooks/
│   └── 01_data_reconnaissance.ipynb
│
├── okf/
│   └── business knowledge and rules
│
├── semantic_layer/
│   └── data and metric definitions
│
├── src/
│   └── supporting project utilities
│
├── tools/
│   └── investigation tools
│
├── tests/
│
├── requirements.txt
└── README.md

```
---

## 🛠️ Tech Stack

- **Python** — core implementation
- **DuckDB** — analytical database
- **SQL** — deterministic data investigation
- **Google Gemini** — LLM for Text-to-SQL and reasoning
- **VS Code** — development and experimentation

---

## ⚠️ Current Limitations

ShelfSleuth is a **research and portfolio prototype**, not a production deployment.

- Small evaluation dataset and limited live test coverage
- Dependent on LLM API availability and request quotas
- LLM-generated SQL and reasoning can still contain errors
- Business knowledge is currently relatively small and manually defined
- No production-grade monitoring, authentication, or deployment infrastructure
- 
---

## 🎯 Purpose

This project was created as a hands-on exercise to understand how **OKF, semantic layers, and Text-to-SQL** work together in an AI-powered analytics workflow.

---

# 👨‍💻 Author

**Siddharth Ranganatha**
