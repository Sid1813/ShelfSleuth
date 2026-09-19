# Define the ShelfSleuth pipeline that coordinates all agents
# and investigation tools


from agents.text_to_sql_agent import TextToSQLAgent

from agents.knowledge_agent import KnowledgeAgent

from agents.root_cause_agent import RootCauseAgent

from agents.action_planner_agent import ActionPlannerAgent

from agents.critic_agent import CriticAgent

from okf.loader import load_okf_knowledge


class ShelfSleuthPipeline:

    def __init__(
        self,
        database_connection,
        semantic_context,
        investigation_tool,
    ):

        # Load business knowledge from the OKF Markdown bundle

        knowledge_base = load_okf_knowledge()


        # Create the Text-to-SQL Agent with access to the database
        # and semantic layer

        self.text_to_sql_agent = TextToSQLAgent(
            database_connection=database_connection,
            semantic_context=semantic_context,
        )


        # Create the Knowledge Agent as the OKF retrieval layer

        self.knowledge_agent = KnowledgeAgent(
            knowledge_base=knowledge_base,
        )


        # Create the Root Cause Agent with access to controlled
        # investigation tools

        self.root_cause_agent = RootCauseAgent(
            investigation_tool=investigation_tool,
        )


        # Create the Action Planner Agent

        self.action_planner_agent = ActionPlannerAgent()


        # Create the Critic Agent

        self.critic_agent = CriticAgent()

    # Run the complete ShelfSleuth investigation

    def run(self, question):

        # Convert the user's natural-language question into SQL
        # and execute it
        sql_answer = self.text_to_sql_agent.answer_question(
            question
        )

        # Retrieve only the OKF concepts relevant to the question
        knowledge = self.knowledge_agent.get_knowledge(
            question=question
        )

        # Investigate the initial result using controlled SQL
        # investigations and relevant business knowledge
        root_cause_analysis = self.root_cause_agent.analyze(
            question=question,
            initial_result=sql_answer["result"],
            knowledge=knowledge,
        )

        # Convert the root-cause findings into recommended business actions
        action_plan = self.action_planner_agent.create_action_plan(
            question=question,
            root_cause_analysis=root_cause_analysis,
        )

        # Ask the Critic Agent to validate the reasoning
        # and recommendations
        critic_review = self.critic_agent.review(
            question=question,
            root_cause_analysis=root_cause_analysis,
            action_plan=action_plan,
        )

        # Extract the direct answer already produced by the
        # Root Cause Agent.
        #
        # The Root Cause Agent currently returns its analysis
        # as a dictionary containing a "root_cause" text field.
        root_cause_text = root_cause_analysis.get(
            "root_cause",
            ""
        )

        direct_answer = root_cause_text

        # If the Root Cause Agent uses the expected Markdown
        # structure, extract only the Direct Answer section.
        if "### **Direct Answer**" in root_cause_text:

            direct_answer = root_cause_text.split(
                "### **Direct Answer**",
                1
            )[1]

            if "### **Direct Evidence" in direct_answer:

                direct_answer = direct_answer.split(
                    "### **Direct Evidence",
                    1
                )[0]

            direct_answer = direct_answer.strip()

        # Return the complete investigation and important
        # intermediate outputs
        return {
            "question": question,

            "answer": direct_answer,

            "sql": sql_answer["sql"],

            "sql_result": sql_answer["result"],

            "knowledge": knowledge,

            "root_cause_analysis": root_cause_analysis,

            "action_plan": action_plan,

            "critic_review": critic_review,
        }