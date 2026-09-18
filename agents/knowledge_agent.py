# Define the Knowledge Agent as a lightweight deterministic
# business-knowledge retrieval layer for the OKF bundle


class KnowledgeAgent:

    def __init__(self, knowledge_base):

        # Store the parsed OKF knowledge

        self.knowledge_base = knowledge_base


    # Retrieve the OKF concepts most relevant to a question

    def get_knowledge(self, question=None):

        # If no question is provided, return the complete knowledge base

        if not question:
            return self.knowledge_base


        # Normalize the user's question

        question = question.lower()


        # Define business terms and the OKF concepts they relate to

        concept_keywords = {

            "inventory": {
                "inventory",
                "stock",
                "stockout",
                "coverage",
                "shortage",
                "overstock",
            },

            "demand": {
                "demand",
                "forecast",
                "forecasted",
                "forecasting",
                "bias",
                "sales",
                "sold",
            },

            "store_performance": {
                "store",
                "stores",
                "location",
                "locations",
                "performance",
            },
        }


        # Determine which OKF concepts are relevant to the question

        relevant_concepts = []


        for concept_name, keywords in concept_keywords.items():

            if any(keyword in question for keyword in keywords):

                if concept_name in self.knowledge_base:

                    relevant_concepts.append(concept_name)


        # If no specific concepts were identified,
        # fall back to the complete OKF bundle

        if not relevant_concepts:

            return self.knowledge_base


        # Return only the relevant OKF concepts

        return {
            concept_name: self.knowledge_base[concept_name]
            for concept_name in relevant_concepts
        }
