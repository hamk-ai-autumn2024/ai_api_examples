import os
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chroma_test",
            "path": "db",
        }
    },
    "version": "v1.1",
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0,
            "max_tokens": 1000,
        },
    },
}

# Initialize Memory with the configuration
m = Memory.from_config(config)

# Add a memory
m.add("I'm visiting Paris.", user_id="john")
m.add("I like to cook.", user_id="john")
# Retrieve memories
memories = m.get_all(user_id="john")
print(memories)
