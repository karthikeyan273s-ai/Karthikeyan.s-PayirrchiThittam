from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=4000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=12000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=300
    )

    language: str = Field(
        default="English",
        min_length=2,
        max_length=40
    )

    tone: str = Field(
        default="Formal and professional",
        min_length=2,
        max_length=100
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "dates",
        "language",
        "tone"
    )
    @classmethod
    def strip_values(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty."
            )

        return value


class ExportRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=20,
        max_length=100000
    )

    document_type: str = Field(
        default="Legal Document",
        max_length=120
    )

    terms: str = Field(
        default="",
        max_length=12000
    )

    effective_date: Optional[str] = Field(
        default=None,
        max_length=300
    )

    logo_base64: Optional[str] = None