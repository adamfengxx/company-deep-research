from langchain_core.messages import SystemMessage, HumanMessage
from agent.state import TaskState, Summary
from agent.prompts import SUMMARIZER_PROMPT
from agent.config import get_chat_model

llm = get_chat_model()

async def summarizer_node(state: TaskState) -> dict:
    title = state["title"]
    raw_results = state["raw_results"]

    summarizer_llm = llm.with_structured_output(Summary)
    result = await summarizer_llm.ainvoke([
        SystemMessage(content=SUMMARIZER_PROMPT),
        HumanMessage(content=f"Task: {title}\n\nRaw results:\n{raw_results}"),
    ])

    return {
        "summaries": [result],
        "llm_call": 1,
    }
