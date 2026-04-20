import resend
import markdown
from agent.config import settings

resend.api_key = settings.resend_api_key


async def send_report_email(to: str, query: str, report_markdown: str) -> None:
    html_body = markdown.markdown(report_markdown, extensions=["tables", "fenced_code"])

    resend.Emails.send({
        "from": settings.sender_email,
        "to": to,
        "subject": f"Research Report: {query}",
        "html": html_body,
    })
