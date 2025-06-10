from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models.openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END



    

local_llm = "llama-3.2-3b-instruct"

model = ChatOpenAI(
    base_url="http://192.168.1.4:1234/v1/",
    api_key="lm-studio",
    model=local_llm,
    temperature=0.8,
    streaming=True
)


class AgentState(TypedDict):
    messages: List[HumanMessage]



# def process(state: AgentState) -> AgentState:
#     response = model.invoke(state["messages"])
#     print(f"\nAI: {response.content}")
#     return state

def process(state: AgentState) -> AgentState:
    print("\nAI: ", end="", flush=True)
    streamed_text = ""
    for chunk in model.stream(state["messages"]):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            streamed_text += chunk.content

    state["messages"].append(AIMessage(content=streamed_text))
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("\nEnter: ")