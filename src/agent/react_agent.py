from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt.tool_node import ToolNode
from llm.openai import OpenAIFactory
from tools.search_crountry_tools import get_country_info, get_country_by_code
from prompts.system_prompt import SYSTEM_PROMPT

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

memory = InMemorySaver()

tools = [get_country_info, get_country_by_code]
llm = OpenAIFactory.create_llm()
model_with_tools = llm.bind_tools(tools)

def call_model(state: AgentState) -> dict:
    """Calls the LLM with the current state and returns the response."""
    messages = state["messages"]
    if not messages or not any(isinstance(msg, SystemMessage) for msg in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

call_tools = ToolNode(tools)

def should_continue(state: AgentState) -> str:
    """Decides the next step after calling the LLM."""
    last_message = state["messages"][-1]

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return END
    else:
        return "call_tools"

graph_builder = StateGraph(AgentState)

graph_builder.add_node("call_model", call_model)
graph_builder.add_node("call_tools", call_tools)

graph_builder.add_edge(START, "call_model")
graph_builder.add_edge("call_tools", "call_model")
graph_builder.add_conditional_edges(
    "call_model", 
    should_continue, 
    { END: END, "call_tools": "call_tools" }
)

agent = graph_builder.compile(checkpointer=memory)
