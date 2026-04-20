import os
from langchain_core.messages import SystemMessage, HumanMessage
from agent.state import GlobalState
from agent.prompts import REPORTER_PROMPT
from agent.config import get_chat_model

llm = get_chat_model()

async def reporter_node(state: GlobalState) -> dict:
    query = state["query"]
    summaries = state["summaries"]

    summaries_text = "\n\n".join([
        f"## {s.task_title}\n{s.content}\nReferences: {s.references}"
        for s in summaries
    ])

    result = await llm.ainvoke([
        SystemMessage(content=REPORTER_PROMPT),
        HumanMessage(content=f"Query: {query}\n\nSummaries:\n{summaries_text}"),
    ])

    final_report = result.content

    return {
        "final_report": final_report,
        "llm_call": 1,
    }
