# Define the Action Planner Agent that converts root-cause findings into practical business actions

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


class ActionPlannerAgent:

    def __init__(self):

        # The Action Planner currently does not require any external tools
        pass


    # Send a prompt to Gemini while handling temporary API failures
    def _generate_response(self, prompt, max_retries=2):

        for attempt in range(max_retries + 1):

            try:

                return client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt,
                )

            except errors.ClientError as error:

                # Stop immediately when Gemini quota is exhausted
                if getattr(error, "code", None) == 429:

                    raise RuntimeError(
                        "Gemini API quota has been exhausted. "
                        "Please wait for the quota to reset."
                    ) from error

                raise

            except errors.ServerError as error:

                # Retry temporary server errors such as HTTP 503
                if getattr(error, "code", None) == 503 and attempt < max_retries:

                    time.sleep(2 ** attempt)
                    continue

                raise


    # Convert root-cause findings into recommended business actions
    def create_action_plan(self, question, root_cause_analysis):

        prompt = f"""
You are the Action Planner Agent for ShelfSleuth.

User question:
{question}

Root-cause investigation:
{root_cause_analysis}

Based only on the evidence provided, recommend practical business actions.

For each recommendation:
1. State the action.
2. Explain why it is appropriate.
3. Identify the business persona that should own the action.
4. State what metric should be monitored afterward.

Do not invent facts.
Do not recommend increasing inventory unless the evidence supports an inventory shortage.
"""

        # Ask Gemini to convert the root-cause findings into an actionable plan
        response = self._generate_response(prompt)

        # Return the generated action plan
        return response.text.strip()
