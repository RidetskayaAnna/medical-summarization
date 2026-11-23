from typing import Literal
from pydantic import BaseModel, Field, field_validator


class SummarizationRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Полная история болезни"
    )
    method: Literal["baseline", "zero_shot", "few_shot", "all"] = "all"

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("История болезни не может быть пустой")
        return value


class SummarizationResponse(BaseModel):
    results: dict[str, str] = Field(
        default_factory=dict,
        description="Результаты суммаризации"
    )
    errors: dict[str, str] = Field(
        default_factory=dict,
        description="Ошибки отдельных методов"
    )