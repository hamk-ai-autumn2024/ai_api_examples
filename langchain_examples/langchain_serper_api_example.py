from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

#search = GoogleSerperAPIWrapper()

#model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#search = GoogleSerperAPIWrapper()
#results = search.run("Where was Elvis born?", verbose=False)
#print(results)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
#tool = Tool("serper", GoogleSerperAPIWrapper())
tool = SearchCodeTool()
tools = [tool]
agent = create_structured_chat_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_executor.invoke({"input": "hi"})

# Using with chat history

agent_executor.invoke(
    {
        "input": "what model are you?",
        "chat_history": [
            SystemMessage(content="Respond directly without any preamble."),
            HumanMessage(content="What is the capital of Helsinki?"),
        ],
    }
)