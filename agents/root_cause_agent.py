# Define the Root Cause Agent that interprets controlled investigation evidence using business knowledge


# Import the libraries needed to load our Gemini API key and communicate with Gemini

import os

import time

from dotenv import load_dotenv

from google import genai

from google.genai import errors


# Load environment variables from the project's .env file

load_dotenv()


# Create a Gemini client using the API key stored in the environment

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class RootCauseAgent:

    def __init__(self, investigation_tool, knowledge_base):

        # Store the investigation tool so the agent can access controlled SQL investigations

        self.investigation_tool = investigation_tool


        # Store the business knowledge so the agent can reason using established rules

        self.knowledge_base = knowledge_base


    # Send a prompt to Gemini while handling temporary API failures

    def _generate_response(self, prompt, max_retries=2):

        # Try the Gemini request up to the configured number of retries

        for attempt in range(max_retries + 1):

            try:

                # Send the prompt to Gemini

                return client.models.generate_content(
                    model="gemini-3.6-flash",

                    contents=prompt,
                )


            except errors.ClientError as error:

                # Stop immediately when the Gemini quota is exhausted

                if getattr(error, "code", None) == 429:

                    raise RuntimeError(
                        "Gemini API quota has been exhausted. "
                        "Please wait for the quota to reset."
                    ) from error


                # Re-raise other client errors

                raise


            except errors.ServerError as error:

                # Retry temporary server errors such as HTTP 503

                if getattr(error, "code", None) == 503 and attempt < max_retries:

                    # Wait progressively longer before retrying

                    time.sleep(2 ** attempt)

                    continue


                # Raise the error if retries are exhausted

                raise


    # Investigate the initial result using a controlled investigation

    def analyze(self, question, initial_result):

        # Run the predefined store-level inventory investigation

        investigation_result = (
            self.investigation_tool.store_inventory_comparison()
        )


        # Convert the business knowledge into readable text for Gemini

        knowledge = str(self.knowledge_base)


        # Build a prompt containing the original question and controlled evidence

        prompt = f"""
You are the Root Cause Agent for ShelfSleuth.

User question:
{question}

Initial SQL result:
{initial_result}

Controlled investigation:
Store-level inventory comparison.

Investigation result:
{investigation_result}

Business knowledge:
{knowledge}

Analyze the evidence and identify the most likely root causes.

Clearly distinguish between:
- Direct evidence from the data.
- Business interpretation.
- Hypotheses that require further investigation.

Do not invent facts.
Do not claim causation unless the evidence supports it.
"""


        # Ask Gemini to interpret the controlled investigation evidence

        response = self._generate_response(prompt)


        # Return the investigation evidence and root-cause analysis

        return {
            "investigation": "store_inventory_comparison",

            "investigation_result": investigation_result,

            "root_cause": response.text.strip(),
        }