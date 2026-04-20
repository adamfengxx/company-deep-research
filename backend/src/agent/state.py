"""
The global state and subgraph state
"""
from typing_extensions import TypedDict, Annotated
from pydantic import BaseModel
import operator


class Task(BaseModel):
    title: str
    intent: str


class Summary(BaseModel):
    task_title: str
    content: str
    references: list[str]


class PlannerOutput(BaseModel):
    tasks: list[Task]


# each summary, llm call and tool call is added instead of overwrite
class GlobalState(TypedDict):
    query: str
    tasks: list[Task]
    summaries: Annotated[list[Summary], operator.add]
    llm_call: Annotated[int, operator.add]
    tool_call: Annotated[int, operator.add]
    final_report: str


# Subgraph state for each parallel research branch.
# Channels that overlap with GlobalState (summaries, llm_call, tool_call)
# are automatically merged back using GlobalState's reducers when the subgraph finishes.
# each task has its own state.
class TaskState(TypedDict):
    title: str
    intent: str
    raw_results: str
    summaries: list[Summary]
    llm_call: int
    tool_call: int
