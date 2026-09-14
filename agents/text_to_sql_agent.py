# Define the Text-to-SQL agent that converts natural-language questions into SQL


# Import the libraries needed to load our Gemini API key and communicate with Gemini

import os

from dotenv import load_dotenv

from google import genai


# Load environment variables from the project's .env file

load_dotenv()


# Create a Gemini client using the API key stored in the environment

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class TextToSQLAgent:

    def __init__(self, database_connection, semantic_context):

        # Store the DuckDB connection so the agent can execute SQL

        self.con = database_connection


        # Store the semantic layer so the agent knows what our metrics and dimensions mean

        self.semantic_context = semantic_context


    # Ask Gemini to convert a natural-language question into a SQL query

    def generate_sql(self, question):

        # Build the prompt using our semantic layer and the user's question

        prompt = self.build_prompt(question)


        # Send the prompt to Gemini 3.6 Flash and ask it to generate SQL

        response = client.models.generate_content(
            model="gemini-3.6-flash",

            contents=prompt,
        )


        # Extract the generated SQL from Gemini's response

        sql = response.text.strip()


        # Remove Markdown code fences if Gemini wraps the SQL in ```sql ... ```

        sql = sql.replace("```sql", "").replace("```", "").strip()


        # Return clean SQL that can be executed directly by DuckDB

        return sql


    def execute_sql(self, sql):

        # Execute the SQL query against DuckDB and return the results as a DataFrame

        return self.con.execute(sql).fetchdf()


    # Build the instructions that will be given to the LLM before it generates SQL

    def build_prompt(self, question):

        # Convert the semantic definitions into readable text for the LLM

        semantic_description = str(self.semantic_context)


        # Combine the database information, semantic definitions, and user question

        prompt = f"""
You are a Text-to-SQL agent for ShelfSleuth.

Database table:
retail_inventory

Semantic definitions:
{semantic_description}

User question:
{question}

Generate a SQL query that answers the user's question.
Return only the SQL query.
"""


        return prompt