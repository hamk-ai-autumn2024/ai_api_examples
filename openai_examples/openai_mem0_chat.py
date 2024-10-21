from openai import OpenAI
from mem0 import Memory

# Initialize the OpenAI client
client = OpenAI()  # Use the OPENAI_API_KEY environment variable to authenticate

class PersonalAITutor:
    def __init__(self):
        """
        Initialize the PersonalAITutor with memory configuration and OpenAI client.
        """
        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "chroma_test",
                    "path": "db",
                }
            },
            "version": "v1.1"
        }
        self.memory = Memory.from_config(config)
        self.client = client
        self.app_id = "app-1"

    def ask(self, question, user_id=None):
        """
        Ask a question to the AI and store the relevant facts in memory

        :param question: The question to ask the AI.
        :param user_id: Optional user ID to associate with the memory.
        """
        # Start a streaming chat completion request to the AI
        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            stream=True,
            messages=[
                {"role": "system", "content": "You are a personal AI Tutor."},
                {"role": "user", "content": question}
            ]
        )
        # Store the question in memory
        self.memory.add(question, user_id=user_id, metadata={"app_id": self.app_id})

        # Print the response from the AI in real-time
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

    def get_memories(self, user_id=None):
        """
        Retrieve all memories associated with the given user ID.

        :param user_id: Optional user ID to filter memories.
        :return: List of memories.
        """
        return self.memory.get_all(user_id=user_id)

# Instantiate the PersonalAITutor
ai_tutor = PersonalAITutor()

# Define a user ID
user_id = "john_doe"

# Ask a question
ai_tutor.ask("I am learning introduction to CS. What is queue? Briefly explain.", user_id=user_id)
