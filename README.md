# AI Subscription Manager

An agentic AI-powered subscription management system that helps users track monthly subscriptions, monitor spending against a budget, receive renewal reminders, and get intelligent recommendations for reducing subscription costs.

The project uses **Groq** as the LLM provider, the **OpenAI Agents SDK** for agent/tool orchestration, and **SQLite** for persistent memory.

---

## Project Overview

Managing multiple subscriptions can make it difficult to keep track of monthly expenses and renewal dates.

This project provides an AI Subscription Manager that can:

- Add and remember active subscriptions
- Calculate total monthly subscription spending
- Track a user's monthly subscription budget
- Detect when the user exceeds their budget
- Analyze active subscriptions and recommend which subscription(s) could be cancelled to get back under budget
- Calculate estimated yearly subscription expenses
- Track subscription renewal dates
- Find upcoming subscription renewals
- Maintain persistent subscription data using SQLite

The system is **agentic** because the AI agent can decide which tools it needs to call based on the user's request and reason over the information returned by those tools.

---

# Features

## 1. Subscription Management

Users can add subscriptions using natural language.

Example:

```text
Add Netflix for ₹649, renewing on 2026-09-01.
```

The agent extracts the relevant information and calls the `add_subscription` tool.

---

## 2. Monthly Spending Tracking

The agent can calculate the total monthly cost of all active subscriptions.

Example:

```text
How much am I spending every month?
```

---

## 3. Persistent Memory

The application uses SQLite to permanently store subscription information.

Stored information includes:

- Subscription name
- Monthly cost
- Renewal date
- Active/inactive status
- Monthly budget

The data remains available even after the application is closed and restarted.

### Memory architecture

```text
AI Agent
   |
   v
Tools
   |
   v
SQLite Database
   |
   v
subscriptions.db
```

---

# Agentic Budget Management

This is the main agentic feature of the project.

The user can define a monthly subscription budget.

Example:

```text
Set my monthly subscription budget to ₹2000.
```

The agent stores the budget in persistent memory.

If the user's spending exceeds the budget, the agent can analyze the active subscriptions and recommend a cancellation strategy.

### Example

Suppose the user has:

```text
Netflix       ₹649
Spotify       ₹1199
Amazon Prime  ₹299
```

Total:

```text
₹649 + ₹1199 + ₹299 = ₹2147
```

Budget:

```text
₹2000
```

The user asks:

```text
What subscription should I consider cancelling to get back under budget?
```

The agent retrieves:

1. Current budget
2. Current monthly total
3. Active subscriptions

It then evaluates possible cancellation choices.

For example:

```text
Current spending = ₹2147
Budget = ₹2000
Overspending = ₹147

Cancel Amazon Prime:

₹2147 - ₹299 = ₹1848
```

The agent can recommend Amazon Prime because removing it would bring the estimated monthly spending below the budget.

### Important

The agent **does not automatically cancel subscriptions**.

It only provides a recommendation.

```text
User
  |
  v
Agent
  |
  +--> Get Budget
  |
  +--> Get Monthly Total
  |
  +--> Get Subscriptions
  |
  v
Reason About Possible Cancellations
  |
  v
Recommendation
  |
  v
User
```

This decision-making process is the primary agentic component of the project.

---

# Yearly Cost View

The application can calculate the estimated yearly subscription cost.

Example:

```text
How much will my subscriptions cost per year?
```

If the monthly total is:

```text
₹2147
```

the yearly estimate is:

```text
₹2147 × 12 = ₹25764
```

---

# Renewal Date Tracking

Subscriptions can optionally have a renewal date.

Example:

```text
Add Netflix for ₹649, renewing on 2026-09-01.
```

The application stores the renewal date in SQLite.

Users can ask:

```text
Which subscriptions are renewing soon?
```

or:

```text
Which subscriptions are renewing in the next 7 days?
```

The agent uses the renewal-date tool to retrieve matching subscriptions.

> **Note:** The current implementation checks upcoming renewals when the user asks; it does not send automatic push/email notifications.

---

# How the Agent Works

The project follows a tool-using agent architecture.

```text
                         USER
                           |
                           v
                    +-------------+
                    |  AI AGENT   |
                    |   (Groq)    |
                    +------+------+
                           |
                    Decides which
                    tool to use
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
 add_subscription   get_monthly_total   get_subscriptions
        |                  |                  |
        +------------------+------------------+
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
 set_monthly_budget                  get_monthly_budget
        |                                     |
        +------------------+------------------+
                           |
                 +---------+---------+
                 |                   |
                 v                   v
          get_yearly_cost    get_upcoming_renewals
                 |                   |
                 +---------+---------+
                           |
                           v
                    +-------------+
                    |   SQLite    |
                    |   Memory    |
                    +-------------+
```

The agent does not simply execute a fixed sequence of instructions. The LLM determines which tool(s) are relevant to the user's request.

---

# Tools

| Tool | Purpose |
|---|---|
| `add_subscription()` | Adds a new subscription |
| `get_monthly_total()` | Calculates total monthly spending |
| `get_subscriptions()` | Retrieves active subscriptions |
| `set_monthly_budget()` | Stores/updates monthly budget |
| `get_monthly_budget()` | Retrieves current budget |
| `get_yearly_cost()` | Calculates estimated yearly spending |
| `get_upcoming_renewals()` | Finds upcoming renewal dates |

---

# Database Schema

The application uses SQLite.

## `subscriptions`

| Column | Description |
|---|---|
| `id` | Unique subscription ID |
| `name` | Subscription name |
| `cost` | Monthly subscription cost |
| `renewal_date` | Optional renewal date |
| `active` | Whether the subscription is active |

## `settings`

| Column | Description |
|---|---|
| `key` | Setting name |
| `value` | Setting value |

The monthly budget is stored using:

```text
key = monthly_budget
```

---

# Project Structure

```text
ai-subscription-manager/
│
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── database.py
│   ├── main.py
│   └── tools.py
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── subscriptions.db
```

### File Responsibilities

### `src/agent.py`

Creates and configures the AI agent.

- Connects to Groq
- Configures the LLM
- Defines agent instructions
- Registers tools

### `src/tools.py`

Contains functions exposed to the AI agent.

- Adds subscriptions
- Retrieves subscription information
- Calculates spending
- Manages budget
- Calculates yearly costs
- Finds upcoming renewals

### `src/database.py`

Handles persistent SQLite storage.

- Creates database tables
- Stores subscriptions
- Retrieves subscriptions
- Calculates totals
- Stores/retrieves budget

### `src/main.py`

Application entry point.

- Initializes the database
- Starts the agent
- Accepts user input
- Sends requests to the agent
- Displays responses

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Groq | LLM provider |
| GPT-OSS-20B | AI model |
| OpenAI Agents SDK | Agent and tool orchestration |
| SQLite | Persistent memory/database |
| python-dotenv | Environment variable management |

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-subscription-manager.git
cd ai-subscription-manager
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Groq API Key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Do **not** commit this file to GitHub.

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
*.pyc
subscriptions.db
.pytest_cache/
```

---

# Running the Application

From the project root:

```bash
python src/main.py
```

You should see:

```text
==================================================
       AI SUBSCRIPTION MANAGER
==================================================

Type 'exit' to quit.

You:
```

You can now interact with the AI agent.

---

# Example Usage

### Add subscriptions

```text
You: Add Netflix for ₹649, renewing on 2026-09-01.
Agent: Netflix has been added successfully.
```

### View subscriptions

```text
You: What subscriptions do I have?
```

### Check monthly spending

```text
You: How much am I spending every month?
```

### Set budget

```text
You: Set my monthly subscription budget to ₹2000.
```

### Check budget

```text
You: Am I within my monthly subscription budget?
```

### Get cancellation recommendation

```text
You: What should I cancel to get back under budget?
```

### Get yearly cost

```text
You: How much will my subscriptions cost per year?
```

### Check renewals

```text
You: Which subscriptions are renewing soon?
```

or:

```text
You: Which subscriptions are renewing in the next 7 days?
```

---

# Testing

The project was tested for:

- Adding subscriptions
- Multiple subscriptions
- Viewing active subscriptions
- Monthly spending calculation
- Yearly spending calculation
- Setting a monthly budget
- Detecting budget overruns
- Generating cancellation recommendations
- Adapting recommendations when the budget changes
- Finding upcoming renewals
- Handling subscriptions without renewal dates
- Handling an empty database
- Handling a missing budget
- Rejecting invalid budgets
- Persistence after application restart

### Example agentic test

Given:

```text
Netflix       ₹649
Spotify       ₹1199
Amazon Prime  ₹299

Budget = ₹2000
```

The agent determines:

```text
Total = ₹2147
Over budget = ₹147
```

It evaluates possible cancellation options and recommends an option that brings spending below the budget.

---

# Security

The Groq API key is stored in an environment variable rather than hard-coded in the source code.

```text
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` to GitHub.

The SQLite database is also excluded from version control because it contains local application state.

---

# Limitations

1. The AI recommends subscriptions for cancellation but does not automatically cancel them.
2. Actual cancellation must be performed manually by the user.
3. Renewal reminders are generated when the user asks the agent rather than being delivered as external notifications.
4. Subscription costs are assumed to be monthly.
5. Yearly cost is calculated as monthly cost × 12.
6. The application currently uses SQLite for local persistent storage.
7. The system requires a valid Groq API key and internet connectivity.

---

# Future Improvements

Possible future improvements include:

- Add/remove/update subscription tools
- Automatic renewal notifications
- Email or mobile notifications
- Authentication and multiple user accounts
- Web-based dashboard
- Subscription spending charts
- Category-based subscription analysis
- Duplicate subscription detection
- Cheaper subscription recommendations
- Yearly savings analysis
- Recurring payment history
- Cloud database support
- More sophisticated cancellation optimization

---

# Academic Objective

This project demonstrates fundamental concepts of **Agentic AI**, including:

- LLM-based decision making
- Tool calling
- Agent instructions
- Persistent memory
- State retrieval
- Multi-step reasoning
- Goal-oriented behavior
- External tool integration
- Structured data storage

The project demonstrates how an LLM can move beyond simple question answering by interacting with external tools and using their results to make decisions.

---

# What Makes This Project Agentic?

A conventional application might contain fixed logic such as:

```python
if monthly_total > budget:
    return "Cancel Amazon Prime"
```

This project instead gives the agent access to:

```text
get_monthly_budget()
get_monthly_total()
get_subscriptions()
```

The agent can then:

```text
1. Determine what information it needs
2. Call the appropriate tools
3. Observe the returned information
4. Analyze the current subscription state
5. Evaluate possible actions
6. Provide a recommendation
```

Therefore, the cancellation recommendation is based on the **current state of the user's subscriptions and budget**, rather than a fixed hard-coded response.

---

# High-Level Workflow

```text
                 User Request
                      |
                      v
                +-----------+
                |   Agent   |
                +-----+-----+
                      |
              Decide what tools
                  are needed
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Budget       Total    Subscriptions
          |           |           |
          +-----------+-----------+
                      |
                      v
                 AI Reasoning
                      |
                      v
                Final Response
```

---

# Author

**Suprit Das**

CA1 - CSE476 (Agentic AI and Intelligent Automation)

---


