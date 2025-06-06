from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END



    

local_llm = "deepseek/deepseek-r1-0528-qwen3-8b"

model = ChatOpenAI(
    base_url="http://192.168.1.4:1234/v1/",
    api_key="lm-studio",
    model=local_llm,
    temperature=0.0
)


class AgentState(TypedDict):
    messages: List[HumanMessage]



def process(state: AgentState) -> AgentState:
    response = model.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")