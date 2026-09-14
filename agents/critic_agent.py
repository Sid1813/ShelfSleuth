# Define the Critic Agent that validates the reasoning and recommendations produced by other agents


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


class CriticAgent:

    def __init__(self):

        # The Critic currently does not require any external tools

        pass


    # Review the root-cause analysis and action plan for unsupported reasoning

    def review(self, question, root_cause_analysis, action_plan):

        # Build a prompt containing the reasoning and recommendations that need to be checked

        prompt = f"""
You are the Critic Agent for ShelfSleuth.

User question:
{question}

Root-cause analysis:
{root_cause_analysis}

Action plan:
{action_plan}

Review the analysis and recommendations.

Check for:
1. Claims that are not supported by the available evidence.
2. Unsupported assumptions or causal claims.
3. Recommendations that do not logically follow from the evidence.
4. Missing important caveats.
5. Whether the recommended actions have clear business ownership.

Return your review in this structure:

VERDICT:
PASS or NEEDS_REVISION

ISSUES:
List the specific issues found.

RECOMMENDATIONS:
State what should be changed if revision is needed.

Do not invent additional facts.
"""


        # Ask Gemini to critically evaluate the previous agents' outputs

        response = client.models.generate_content(
            model="gemini-3.6-flash",

            contents=prompt,
        )


        # Return the critic's evaluation

        return response.text.strip()