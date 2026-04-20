from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.data_models import Report


async def save_report(
    db: AsyncSession,
    query: str,
    final_report: str,
    llm_call: int,
    tool_call: int,
) -> Report:
    report = Report(
        query=query,
        final_report=final_report,
        llm_call=llm_call,
        tool_call=tool_call,
    )
    try:
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report
    except Exception:
        await db.rollback()
        raise


async def get_report(db: AsyncSession, report_id: str) -> Report | None:
    result = await db.execute(select(Report).where(Report.id == report_id))
    return result.scalar_one_or_none()


async def list_reports(db: AsyncSession) -> list[Report]:
    result = await db.execute(select(Report).order_by(Report.created_at.desc()))
    return list(result.scalars().all())
