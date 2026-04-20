from pydantic import BaseModel
from datetime import datetime


class ResearchRequest(BaseModel):
    query: str


class ResearchResponse(BaseModel):
    report_id: str
    query: str
    final_report: str
    llm_call: int
    tool_call: int
    created_at: datetime


class ReportSummary(BaseModel):
    report_id: str
    query: str
    llm_call: int
    tool_call: int
    created_at: datetime


class SendEmailRequest(BaseModel):
    to: str


class SendEmailResponse(BaseModel):
    message: str
