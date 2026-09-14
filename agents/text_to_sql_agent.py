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

    def generate_sql(self, question, previous_sql=None, sql_error=None):

        # Build the initial prompt using our semantic layer and the user's question

        prompt = self.build_prompt(
            question=question,

            previous_sql=previous_sql,

            sql_error=sql_error,
        )


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


    # Execute SQL against DuckDB

    def execute_sql(self, sql):

        # Execute the SQL query and return the results as a DataFrame

        return self.con.execute(sql).fetchdf()


    # Run the complete Text-to-SQL process with an automatic error-correction loop

    def answer_question(self, question, max_retries=2):

        # Generate the first SQL query from the user's question

        generated_sql = self.generate_sql(question)


        # Try executing the generated SQL

        for attempt in range(max_retries + 1):

            try:

                # Execute the SQL and return the result if it succeeds

                result = self.execute_sql(generated_sql)

                return {
                    "question": question,

                    "sql": generated_sql,

                    "result": result,

                    "attempts": attempt + 1,
                }


            except Exception as error:

                # Stop retrying if the maximum number of attempts has been reached

                if attempt == max_retries:

                    raise error


                # Convert the database error into text so Gemini can understand what went wrong

                sql_error = str(error)


                # Ask Gemini to generate corrected SQL using the failed SQL and database error

                generated_sql = self.generate_sql(
                    question=question,

                    previous_sql=generated_sql,

                    sql_error=sql_error,
                )


    # Build the instructions that will be given to the LLM before it generates SQL

    def build_prompt(self, question, previous_sql=None, sql_error=None):

        # Convert the semantic definitions into readable text for the LLM

        semantic_description = str(self.semantic_context)


        # Start building the prompt with the database and semantic-layer information

        prompt = f"""
You are a Text-to-SQL agent for ShelfSleuth.

Database table:
retail_inventory

Semantic definitions:
{semantic_description}

User question:
{question}

Generate a SQL query that answers the user's question.

Only generate read-only SQL queries.
Use SELECT statements only.
Return only the SQL query.
"""


        # Add the previous failed SQL and database error when the agent is retrying

        if previous_sql and sql_error:

            prompt += f"""

The previous SQL query failed.

Previous SQL:
{previous_sql}

Database error:
{sql_error}

Correct the SQL query based on this error.

Return only the corrected SQL query.
"""


        return prompt