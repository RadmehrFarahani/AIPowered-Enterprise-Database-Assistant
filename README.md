# AI-Powered Enterprise Database Assistant

An intelligent database assistant that allows users to interact with company data using natural language instead of writing SQL queries manually.

The application uses **Llama 3.2** through **Ollama** and **LangChain** to understand user questions, inspect the database schema, generate appropriate SQLite queries, and retrieve the requested information. It also includes basic SQL validation to prevent potentially destructive database operations.

### Key Features

- 💬 Natural language interaction with company data
- 🧠 Llama 3.2 for natural language understanding and SQL generation
- 🔗 LangChain-based LLM integration
- 🗄️ SQLite database integration
- 🔒 SQL validation and restricted query execution
- 📊 Tabular result visualization with Streamlit
- ⚡ Fully local LLM execution using Ollama

### Tech Stack

**Python · LangChain · Ollama · Llama 3.2 · SQLite · SQLAlchemy · Pandas · Streamlit**

### How It Works

**User Question → Database Schema → LLM → SQL Query → Security Validation → Database → Results**

For example, users can ask:

> "What are the top 10 best-selling products?"

Instead of writing SQL manually, the assistant generates the required query, executes it against the database, and presents the results through the Streamlit interface.

This project demonstrates a practical implementation of an **LLM-powered enterprise data assistant** and explores the integration of Large Language Models with structured business data.
