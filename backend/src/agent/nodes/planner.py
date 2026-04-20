"""
The planner node. The llm model need to understand the query and generate 
several tasks to solve the query.
"""
import logging
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from agent.state import GlobalState, PlannerOutput
from agent.prompts import PLANNER_PROMPT
from agent.config import get_chat_model

logger = logging.getLogger(__name__)

llm = get_chat_model()

# async to be consistent with other nodes.
async def planner_node(state: GlobalState) -> dict:
    # date time responsible to let llm know the date 
    today = datetime.now().strftime("%B %d, %Y")
    query = state["query"]

    try:
        # the output is structured as we set.
        planner_llm = llm.with_structured_output(PlannerOutput)
        result = await planner_llm.ainvoke([
            SystemMessage(content=PLANNER_PROMPT),
            HumanMessage(content=f"Today's date: {today}\n\nQuery: {query}"),
        ])

        return {
            "tasks": result.tasks,
            "llm_call": 1,
        }
    except Exception:
        logger.exception("planner failed", extra={"query": state["query"]})
