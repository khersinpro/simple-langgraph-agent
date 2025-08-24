from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph
from llm.openai import OpenAIFactory

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = OpenAIFactory.create_llm()

def call_model(state: AgentState) -> dict:
    """Calls the LLM with the current state and returns the response."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

graph_builder = StateGraph(AgentState)

graph_builder.add_node("call_model", call_model)
graph_builder.set_entry_point("call_model")
graph_builder.add_edge("call_model", END)

agent = graph_builder.compile()
