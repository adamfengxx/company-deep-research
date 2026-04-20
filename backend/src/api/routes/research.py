import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import ResearchRequest, ResearchResponse
from agent.graph import build_graph
from db.session import get_db
from db.crud import save_report

router = APIRouter()
graph = build_graph()
logger = logging.getLogger(__name__)


@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest, db: AsyncSession = Depends(get_db)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = await graph.ainvoke({"query": request.query})
    except Exception:
        logger.exception("Research request failed", extra={"query": request.query})
        raise HTTPException(status_code=500, detail="Research generation failed")

    report = await save_report(
        db=db,
        query=request.query,
        final_report=result["final_report"],
        llm_call=result["llm_call"],
        tool_call=result["tool_call"],
    )

    return ResearchResponse(
        report_id=report.id,
        query=report.query,
        final_report=report.final_report,
        llm_call=report.llm_call,
        tool_call=report.tool_call,
        created_at=report.created_at,
    )
