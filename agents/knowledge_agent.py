# Define the Knowledge Agent as a lightweight business-knowledge provider


class KnowledgeAgent:

    def __init__(self, knowledge_base):

        # Store the business knowledge so other agents can retrieve it

        self.knowledge_base = knowledge_base


    # Retrieve business knowledge relevant to a question

    def get_knowledge(self, question=None):

        # Return the complete knowledge base for now

        # A more advanced version can later retrieve only relevant knowledge

        return self.knowledge_base