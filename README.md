# Company deep research #

An AI-powered company research system built with LangGraph that automatically
decomposes research queries into parallel tasks, executes them using web search
and financial data tools, and synthesizes a comprehensive markdown report.

## The architecture ##

- **Planner**: Decomposes the query into 3-5 focused research tasks
- **Executer**: ReAct agent that retrieves data using web search and financial APIs
- **Summarizer**: Cleans and structures each task result with references
- **Reporter**: Synthesizes all summaries into a final markdown report

## Tech Stack ##

- **LangGraph** — agent orchestration and parallel workflow (Send API)
- **LangChain** — LLM integration and tool management
- **OpenAi LLM** — LLM backbone
- **Tavily** — web search tool
- **Alpha Vantage MCP** — real-time financial data
- **FastAPI** — REST API server
- **Pydantic** — data validation and structured outputs

## The tools ##


