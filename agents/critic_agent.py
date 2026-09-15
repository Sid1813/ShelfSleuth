# Define the Critic Agent that validates the reasoning and recommendations
# produced by other agents

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


class CriticAgent:

    def __init__(self):

        # The Critic currently does not require any external tools
        pass


    # Send a prompt to Gemini while handling temporary API failures
    def _generate_response(self, prompt, max_retries=2):

        for attempt in range(max_retries + 1):

            try:

                return client.models.generate_content(
                    model="gemini-3.6-flash",
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


    # Review the root-cause analysis and action plan
    # for unsupported reasoning
    def review(self, question, root_cause_analysis, action_plan):

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
        response = self._generate_response(prompt)

        # Return the critic's evaluation
        return response.text.strip()