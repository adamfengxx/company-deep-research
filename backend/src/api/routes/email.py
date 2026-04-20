import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import SendEmailRequest, SendEmailResponse
from db.session import get_db
from db.crud import get_report
from services.email import send_report_email

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/reports/{report_id}/send-email", response_model=SendEmailResponse)
async def send_email(
    report_id: str,
    request: SendEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    report = await get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        await send_report_email(
            to=request.to,
            query=report.query,
            report_markdown=report.final_report,
        )
    except Exception:
        logger.exception("Failed to send email", extra={"report_id": report_id, "to": request.to})
        raise HTTPException(status_code=500, detail="Failed to send email")

    return SendEmailResponse(message=f"Report sent to {request.to}")
