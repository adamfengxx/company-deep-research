"""
This executer node, solve the task using the necessary tools.
We need to first build an agent. React agent. Reasoning and acting forming a loop
to fully solve each tasks. 
"""

from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from agent.state import TaskState
from agent.prompts import EXECUTER_PROMPT
from agent.tools import get_web_search_tool
from agent.mcp_client import mcp_client, get_mcp_tools
from agent.config import get_chat_model, settings

llm = get_chat_model()

# the agent to solve each task
def _build_agent(tools):
    #  bind the llm with tools 
    llm_with_tools = llm.bind_tools(tools)

    async def call_model(state: MessagesState):
        return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

    def should_continue(state: MessagesState) -> str:
        return "tools" if state["messages"][-1].tool_calls else END

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(tools))
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, ["tools", END])
    graph.add_edge("tools", "agent")
    return graph.compile()


async def executer_node(state: TaskState) -> dict:
    today = datetime.now().strftime("%B %d, %Y")
    title = state["title"]
    intent = state["intent"]

    async with mcp_client() as client:
        mcp_tools = await client.get_tools()
        tools = [get_web_search_tool(settings.max_search_results)] + mcp_tools

        agent = _build_agent(tools)
        result = await agent.ainvoke({
            "messages": [
                SystemMessage(content=EXECUTER_PROMPT),
                HumanMessage(content=(
                    f"Today's date: {today}\n"
                    f"Task: {title}\n"
                    f"Intent: {intent}\n"
                    f"Note: If this task requires historical data, "
                    f"focus strictly on the time period mentioned in the intent."
                )),
            ]
        })

    messages = result["messages"]
    llm_call_count = sum(1 for m in messages if isinstance(m, AIMessage))
    tool_call_count = sum(1 for m in messages if isinstance(m, ToolMessage))

    return {
        "raw_results": messages[-1].content,
        "llm_call": llm_call_count,
        "tool_call": tool_call_count,
    }
