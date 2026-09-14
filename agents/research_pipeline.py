# Define the ShelfSleuth pipeline that coordinates all agents and investigation tools


# Import the agents used by the pipeline

from agents.text_to_sql_agent import TextToSQLAgent

from agents.knowledge_agent import KnowledgeAgent

from agents.root_cause_agent import RootCauseAgent

from agents.action_planner_agent import ActionPlannerAgent

from agents.critic_agent import CriticAgent


class ShelfSleuthPipeline:

    def __init__(
        self,
        database_connection,
        semantic_context,
        knowledge_base,
        investigation_tool,
    ):

        # Create the Text-to-SQL Agent with access to the database and semantic layer

        self.text_to_sql_agent = TextToSQLAgent(
            database_connection=database_connection,

            semantic_context=semantic_context,
        )


        # Create the Knowledge Agent as the business-knowledge provider

        self.knowledge_agent = KnowledgeAgent(
            knowledge_base=knowledge_base,
        )


        # Give the Root Cause Agent access to controlled investigation tools and OKF

        self.root_cause_agent = RootCauseAgent(
            investigation_tool=investigation_tool,

            knowledge_base=knowledge_base,
        )


        # Create the Action Planner Agent

        self.action_planner_agent = ActionPlannerAgent()


        # Create the Critic Agent

        self.critic_agent = CriticAgent()


    # Run the complete ShelfSleuth investigation

    def run(self, question):

        # Convert the user's natural-language question into SQL and execute it

        sql_answer = self.text_to_sql_agent.answer_question(
            question
        )


        # Retrieve the deterministic business knowledge from the OKF layer

        knowledge = self.knowledge_agent.get_knowledge(
            question=question
        )


        # Investigate the initial result using controlled SQL investigations

        root_cause_analysis = self.root_cause_agent.analyze(
            question=question,

            initial_result=sql_answer["result"],
        )


        # Convert the root-cause findings into recommended business actions

        action_plan = self.action_planner_agent.create_action_plan(
            question=question,

            root_cause_analysis=root_cause_analysis,
        )


        # Ask the Critic Agent to validate the reasoning and recommendations

        critic_review = self.critic_agent.review(
            question=question,

            root_cause_analysis=root_cause_analysis,

            action_plan=action_plan,
        )


        # Return the complete investigation and all important intermediate outputs

        return {
            "question": question,

            "sql": sql_answer["sql"],

            "sql_result": sql_answer["result"],

            "knowledge": knowledge,

            "root_cause_analysis": root_cause_analysis,

            "action_plan": action_plan,

            "critic_review": critic_review,
        }