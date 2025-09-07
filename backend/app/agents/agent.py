from langgraph.graph import StateGraph, START, END
from app.models.conversation_state import ConversationState, ConversationPhase
from app.agents.router import router
from app.agents.planner import planner
from app.agents.generator import generator
from app.agents.converser import converser

def build_conversational_agent(checkpointer, store):
    """Build the main conversational agent graph (no human approval step)."""
    g = StateGraph(ConversationState)

    # Nodes
    g.add_node("router", router)
    g.add_node("converser", converser)
    g.add_node("planner", planner)
    g.add_node("generator", generator)

    def route_from_router(state: ConversationState) -> str:
        phase = state.get("phase", ConversationPhase.INITIAL)
        nxt = {
            ConversationPhase.INITIAL: "converser",
            ConversationPhase.PLANNING: "planner",
            ConversationPhase.GENERATING: "generator",
            # ↓↓↓ CHANGE: don't end after COMPLETE; allow chatting or editing
            ConversationPhase.COMPLETE: "converser",
            ConversationPhase.CANCELLED: END,
            ConversationPhase.ERROR: END,
        }.get(phase, "converser")  # default to converser, not planner
        import logging
        logging.getLogger(__name__).info(f"Routing phase {phase.value} -> {nxt}")
        return nxt

    g.add_edge(START, "router")
    g.add_conditional_edges("router", route_from_router, {
        "converser": "converser",
        "planner": "planner",
        "generator": "generator",
        END: END,
    })


    # After planning, ALWAYS go generate
    def route_from_planner(state: ConversationState) -> str:
        # Planner now sets phase=GENERATING; this keeps us robust if not set
        phase = state.get("phase")
        return "generator" if phase in (ConversationPhase.GENERATING, ConversationPhase.PLANNING) else END

    g.add_conditional_edges("planner", route_from_planner, {
        "generator": "generator",
        END: END,
    })

    g.add_edge("generator", END)
    g.add_edge("converser", END)

    return g.compile(checkpointer=checkpointer, store=store)
