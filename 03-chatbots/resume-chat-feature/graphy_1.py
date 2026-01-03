from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    streaming=True
)

# ---- STATE ----
class ChatState(TypedDict):
    # messages MUST be BaseMessage objects
    messages: Annotated[list[BaseMessage], add_messages]

# ---- NODE ----
def chat_node(state: ChatState):
    messages = state["messages"]
    ai_message = llm.invoke(messages)
    return {"messages": [ai_message]}

# ---- CHECKPOINTER ----
checkpointer = InMemorySaver()

# ---- GRAPH ----
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# ---- COMPILED GRAPH ----
chatbot = graph.compile(checkpointer=checkpointer)
