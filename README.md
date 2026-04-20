# Company deep research (demo) #

An AI-powered company research system built with LangGraph that automatically
decomposes research queries into parallel tasks, executes them using web search
and financial data tools, and synthesizes a comprehensive markdown report. The md file 
can be downloaded and can be sent to a certain email address.


## The architecture ##

```
planner → produces [task1, task2, task3]
              ↓                                    
Send(task1) → executer instance 1  → summarizer 1 → produce summary 1|
Send(task2) → executer instance 2  → summarizer 2 → produce summary 2| parallel
Send(task3) → executer instance 3  → summarizer 3 → produce summary 3|
              ↓
         reporter (collects all 3 summaries) → produce the final report 
```

- **Planner**: Decomposes the query into 3-5 focused research tasks
- **Executer**: ReAct agent that retrieves data using web search and financial APIs
- **Summarizer**: Cleans and structures each task result with references
- **Reporter**: Synthesizes all summaries into a final markdown report

## Tech Stack ##

- **LangGraph** — agent orchestration and parallel workflow (Send API)
- **LangChain** — LLM integration and tool management
- **OpenAI LLM** — LLM backbone
- **Tavily** — web search tool
- **Alpha Vantage MCP** — real-time financial data
- **FastAPI** — REST API server
- **Pydantic** — data validation and structured outputs

## The tools ##

| Tools | Usage |
|--- | ----|
| Tavily | Web search |
| Alpha Vantage MCP | real-time financial data |
| Resend API | Send email service |


