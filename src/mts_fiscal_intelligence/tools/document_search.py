from models import AppModel, Field

class DocumentSearchQuery(AppModel):
    query: str = Field(min_length=1)
    report_months: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=20)