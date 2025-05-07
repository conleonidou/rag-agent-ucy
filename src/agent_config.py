from agents import Agent

from .context_model import RagAgentContext
from .prompts import (
    TRIAGE_PROMPT,
    RAG_AGENT_PROMPT,
)
from .tools import (
    retrieve_general_documents,
    grade_documents,
)

from dotenv import load_dotenv
import os
load_dotenv()

# Define the new combined RAG Agent
rag_agent = Agent[RagAgentContext](
    model=os.getenv("MODEL"),
    name="RAG Agent",
    handoff_description="An expert agent that retrieves documents based on a user query and then grades them for relevance.",
    instructions=RAG_AGENT_PROMPT,
    tools=[
        retrieve_general_documents, 
        grade_documents
    ],
)

# Define Triage Agent (updated)
triage_agent = Agent[RagAgentContext](
    model=os.getenv("MODEL"),
    name="Triage Agent",
    handoff_description="A triage agent that coordinates the RAG process and formulates the final answer for the user.",
    instructions=TRIAGE_PROMPT,
    handoffs=[
        rag_agent,
    ],
)

# Define the handoff for rag_agent back to triage_agent
rag_agent.handoffs = [triage_agent] # Comment this line to be able to visualize the graph

# Starting agent
starting_agent = triage_agent
# Uncomment this line to visualize the graph
# from agents.extensions.visualization import draw_graph
# draw_graph(starting_agent, filename="agent_graph")