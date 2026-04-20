from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import ResearchResponse, ReportSummary
from db.session import get_db
from db.crud import get_report, list_reports

router = APIRouter()


@router.get("/reports", response_model=list[ReportSummary])
async def get_all_reports(db: AsyncSession = Depends(get_db)):
    reports = await list_reports(db)
    return [
        ReportSummary(
            report_id=r.id,
            query=r.query,
            llm_call=r.llm_call,
            tool_call=r.tool_call,
            created_at=r.created_at,
        )
        for r in reports
    ]


@router.get("/reports/{report_id}", response_model=ResearchResponse)
async def get_one_report(report_id: str, db: AsyncSession = Depends(get_db)):
    report = await get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ResearchResponse(
        report_id=report.id,
        query=report.query,
        final_report=report.final_report,
        llm_call=report.llm_call,
        tool_call=report.tool_call,
        created_at=report.created_at,
    )


@router.get("/reports/{report_id}/download")
async def download_report(report_id: str, db: AsyncSession = Depends(get_db)):
    report = await get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    filename = f"report_{report_id[:8]}.md"
    return Response(
        content=report.final_report,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
