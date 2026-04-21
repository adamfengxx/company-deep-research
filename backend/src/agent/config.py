from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from langchain_openai import ChatOpenAI

_env_path = Path(__file__).parents[2] / ".env"  # backend/src/agent -> backend/.env

# To manage the model, api etc.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_path,
        env_file_encoding="utf-8",
    )

    temperature: float = 0
    openai_api_key: str
    tavily_api_key: str
    alphavantage_api_key: str

    model_name: str = "gpt-4o-mini" #default value
    max_search_results: int = 5

    # Resend
    resend_api_key: str
    sender_email: str = "onboarding@resend.dev"

    # Database
    database_url: str

    @field_validator("database_url", mode="before")
    @classmethod
    def fix_database_url(cls, v: str) -> str:
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v


settings = Settings()


def get_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.model_name,
        api_key=settings.openai_api_key,
        temperature=settings.temperature
    )

# os.getenv("...") Get the value directly from our env. file 
# No need for settings like a bridge.
# settings is a better way to get those values in organized way.   
