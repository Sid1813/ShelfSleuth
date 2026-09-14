# Define the Action Planner Agent that converts root-cause findings into practical business actions


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


class ActionPlannerAgent:

    def __init__(self):

        # The Action Planner currently does not require any external tools

        pass


    # Convert root-cause findings into recommended business actions

    def create_action_plan(self, question, root_cause_analysis):

        # Build a prompt containing the investigation evidence and root-cause findings

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

        response = client.models.generate_content(
            model="gemini-3.6-flash",

            contents=prompt,
        )


        # Return the generated action plan

        return response.text.strip()