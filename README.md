# ShelfSleuth 🔎

### AI-Powered Retail Inventory Investigation & Root-Cause Analysis

ShelfSleuth is an agentic AI system that turns natural-language retail questions into **data-backed investigations and actionable business recommendations**.

Instead of simply generating SQL or returning a number, ShelfSleuth follows an investigation workflow:

> **Question → SQL → Evidence → Business Context → Root Cause → Action → Critique**

The project combines a **semantic layer**, **business knowledge (OKF)**, **Text-to-SQL**, and specialized reasoning agents to investigate retail inventory and demand problems.

---

## 🎯 Problem

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

ShelfSleuth is designed to bridge that gap.

---

## 💡 What ShelfSleuth Does

A user can ask a question in natural language:

> **"Which store has the lowest average inventory?"**

ShelfSleuth then:

1. Understands the retail data model and business terminology.
2. Generates SQL to answer the question.
3. Executes the SQL against the database.
4. Retrieves relevant business knowledge.
5. Investigates the result in a broader business context.
6. Identifies potential root causes.
7. Generates operational recommendations.
8. Critically reviews the final investigation.

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
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
             ┌───────────────┐        ┌─────────────────┐
             │ Semantic Layer│        │ OKF / Business  │
             │               │        │ Knowledge       │
             │ Data meaning  │        │ Business rules  │
             └───────┬───────┘        └────────┬────────┘
                     │                         │
                     └────────────┬────────────┘
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
