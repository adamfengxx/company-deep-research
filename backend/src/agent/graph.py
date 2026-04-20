from langgraph.graph import StateGraph, END
from langgraph.types import Send
from agent.state import GlobalState, TaskState
from agent.nodes import planner_node, executer_node, summarizer_node, reporter_node


# --- Worker subgraph (runs once per task in parallel) ---
# Each branch has its own isolated TaskState so raw_results never bleed between branches.
# Channels that overlap with GlobalState (summaries, llm_call, tool_call) are
# automatically merged back into GlobalState using GlobalState's reducers (operator.add).
def build_worker_graph():
    worker = StateGraph(TaskState)
    worker.add_node("executer", executer_node)
    worker.add_node("summarizer", summarizer_node)
    worker.set_entry_point("executer")
    worker.add_edge("executer", "summarizer")
    worker.add_edge("summarizer", END)
    return worker.compile()


# --- Main graph ---
def route_tasks(state: GlobalState) -> list[Send]:
    return [
        Send("worker", {
            "title": task.title,
            "intent": task.intent,
            "raw_results": "",
            "summaries": [],
            "llm_call": 0,
            "tool_call": 0,
        })
        for task in state["tasks"]
    ]


def build_graph():
    worker_graph = build_worker_graph()

    graph = StateGraph(GlobalState)
    graph.add_node("planner", planner_node)
    graph.add_node("worker", worker_graph)   # subgraph as a node
    graph.add_node("reporter", reporter_node)

    graph.set_entry_point("planner")
    graph.add_conditional_edges("planner", route_tasks, ["worker"])
    graph.add_edge("worker", "reporter")
    graph.add_edge("reporter", END)

    return graph.compile()
