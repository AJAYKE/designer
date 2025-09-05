from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from typing import Literal, Dict, Any
from app.models.conversation_state import ConversationState, ConversationPhase
from app.core.config import settings
from app.agents.message_routing_agent import message_routing_agent
from app.agents.human_feedback_handler import human_feedback_handler
from app.agents.parallel_generation_agent import parallel_generation_agent
from app.agents.planner import planning_agent
from app.agents.conversation_management_agent import conversation_management_agent

def build_conversational_agent(checkpointer, store):
    
    workflow = StateGraph(ConversationState)

    # Nodes
    workflow.add_node("message_router", message_routing_agent)
    workflow.add_node("planner", planning_agent)
    workflow.add_node("feedback_handler", human_feedback_handler)  # Interruption point
    workflow.add_node("parallel_generator", parallel_generation_agent)
    workflow.add_node("conversation_manager", conversation_management_agent)

    # Routing from message_router -> next step (returns KEYS below)
    def route_conversation(state: ConversationState) -> str:
        phase = state.get("phase", ConversationPhase.INITIAL)
        if phase == ConversationPhase.INITIAL:
            return "planner"
        elif phase == ConversationPhase.AWAITING_APPROVAL:
            # Keep returning the KEY "human_feedback" which maps to the node "feedback_handler"
            return "human_feedback"
        elif phase == ConversationPhase.GENERATING:
            return "parallel_generator"
        else:
            return "conversation_manager"

    # After feedback, return the KEYS expected by the mapping below
    def determine_next_step(state: ConversationState) -> str:
        feedback = state.get("human_feedback", {})
        if feedback.get("action") == "approved":
            return "approved"
        elif feedback.get("action") == "edit_plan":
            return "edit_plan"
        elif feedback.get("action") == "cancel":
            return "cancel"
        else:
            return "conversation_manager"

    # Graph
    workflow.add_edge(START, "message_router")
    workflow.add_conditional_edges(
        "message_router",
        route_conversation,
        {
            "planner": "planner",
            "human_feedback": "feedback_handler",  # KEY -> NODE
            "parallel_generator": "parallel_generator",
            "conversation_manager": "conversation_manager",
        },
    )

    workflow.add_edge("planner", "feedback_handler")

    workflow.add_conditional_edges(
        "feedback_handler",
        determine_next_step,
        {
            "approved": "parallel_generator",       # KEY -> NODE
            "edit_plan": "planner",
            "cancel": END,
            "conversation_manager": "conversation_manager",
        },
    )

    workflow.add_edge("parallel_generator", "conversation_manager")
    workflow.add_edge("conversation_manager", END)

    return workflow.compile(
        checkpointer=checkpointer,
        store=store,
        interrupt_before=["feedback_handler"],  # not "human_feedback"
    )
