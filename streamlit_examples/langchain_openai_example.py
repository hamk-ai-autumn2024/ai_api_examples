from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

# assumes OPENAI_API_KEY is set in the environment
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
parser = StrOutputParser()

messages = [
    SystemMessage(content="Translate the following from English into Italian. Output directly without any preambles."),
    HumanMessage(content="Hi! How are you doing today?"),
]
result = model.invoke(messages)
parser.invoke(result)
print(result.content)
