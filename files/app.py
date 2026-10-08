import streamlit as st
import pandas as pd

from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate

from sqlalchemy import create_engine


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="NovaTech AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# Title
# ==========================================

st.title("🤖 NovaTech AI Assistant")

st.write(
    "Ask questions about products, employees, "
    "customers, sales and purchases."
)


# ==========================================
# Database
# ==========================================

db = SQLDatabase.from_uri(
    "sqlite:///novatech.db"
)

engine = create_engine(
    "sqlite:///novatech.db"
)


# ==========================================
# Ollama
# ==========================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# ==========================================
# SQL Prompt
# ==========================================

prompt = PromptTemplate.from_template("""
You are an expert SQL developer.

You have access to a SQLite company database.

Database schema:

{schema}

Convert the user's question into a valid SQLite SQL query.

User question:

{question}

Rules:

1. Return ONLY the SQL query.
2. Do NOT use markdown.
3. Do NOT use ```sql.
4. Do NOT explain anything.
5. Use only tables and columns that exist in the schema.
6. Generate SELECT queries only.
""")


# ==========================================
# User Input
# ==========================================

question = st.text_input(
    "💬 Ask your question:",
    placeholder="Example: What are the top 10 best-selling products?"
)


button = st.button(
    "🔍 Search",
    use_container_width=True
)


# ==========================================
# Main Logic
# ==========================================

if button:

    if not question:

        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 Analyzing your question..."):

            try:

                # ----------------------------------
                # Get database schema
                # ----------------------------------

                schema = db.get_table_info()


                # ----------------------------------
                # Create prompt
                # ----------------------------------

                final_prompt = prompt.format(
                    schema=schema,
                    question=question
                )


                # ----------------------------------
                # Generate SQL
                # ----------------------------------

                response = llm.invoke(final_prompt)


                # ----------------------------------
                # Get SQL from response
                # ----------------------------------

                query = str(response.content).strip()


                # ----------------------------------
                # Remove Markdown
                # ----------------------------------

                query = query.replace("```sql", "")
                query = query.replace("```", "")

                query = query.strip()


                # ----------------------------------
                # Security Check
                # ----------------------------------

                forbidden_words = [
                    "DROP",
                    "DELETE",
                    "UPDATE",
                    "INSERT",
                    "ALTER",
                    "CREATE"
                ]

                upper_query = query.upper()


                if any(
                    word in upper_query
                    for word in forbidden_words
                ):

                    st.error(
                        "This query is not allowed."
                    )

                    st.stop()


                # ----------------------------------
                # Execute SQL
                # ----------------------------------

                df = pd.read_sql_query(
                    query,
                    engine
                )


                # ----------------------------------
                # Display Result
                # ----------------------------------

                st.success(
                    "Information retrieved successfully."
                )

                st.subheader("📊 Results")

                if df.empty:

                    st.info(
                        "No matching records were found."
                    )

                else:

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )


            except Exception as e:

                st.error(
                    "Sorry, I couldn't retrieve the requested information."
                )

                st.caption(
                    f"Error: {e}"
                )