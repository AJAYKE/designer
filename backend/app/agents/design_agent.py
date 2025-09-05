from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from app.models.design_state import DesignState
from app.core.config import settings
from app.agents.planner import planning_agent
from app.agents.generator import generation_agent  
from app.agents.progress_tracker import progress_tracking_agent

async def create_design_agent():
    """
    Create the enhanced LangGraph agent with async postgres checkpointer
    """
    
    # Initialize async postgres components
    checkpointer = AsyncPostgresSaver.from_conn_string(settings.DATABASE_URL)
    store = AsyncPostgresStore.from_conn_string(settings.DATABASE_URL)
    
    # Create the state graph
    workflow = StateGraph(DesignState)
    
    # Add nodes
    workflow.add_node("planner", planning_agent)
    workflow.add_node("screen_generator", generation_agent)
    workflow.add_node("progress_tracker", progress_tracking_agent)
    
    # Define conditional edges
    def should_generate_screens(state: DesignState) -> str:
        if state["plan_approved"]:
            return "screen_generator"
        else:
            return "progress_tracker"  # Wait for approval
    
    def continue_generation(state: DesignState) -> str:
        if state["current_screen_index"] < len(state["design_plan"]["screens"]):
            return "screen_generator"  # Generate next screen
        else:
            return "progress_tracker"  # All screens complete
    
    # Build the workflow
    workflow.add_edge(START, "planner")
    workflow.add_conditional_edges(
        "planner",
        should_generate_screens,
        {
            "screen_generator": "screen_generator",
            "progress_tracker": "progress_tracker"
        }
    )
    workflow.add_conditional_edges(
        "screen_generator", 
        continue_generation,
        {
            "screen_generator": "screen_generator",
            "progress_tracker": "progress_tracker"
        }
    )
    workflow.add_edge("progress_tracker", END)
    
    # Compile with async postgres checkpointer and store
    return workflow.compile(
        checkpointer=checkpointer,
        store=store
    ), checkpointer, store
