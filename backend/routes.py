from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from backend.schemas import (
    DocumentRequest,
    ExportRequest
)

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.exporters import (
    format_txt,
    format_docx,
    format_pdf,
    format_html_preview
)

from backend.utils import safe_filename


router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    tags=["documents"]
)
def generate(request: DocumentRequest):

    try:

        text = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
            request.language,
            request.tone
        )

        return {
            "document_type":
                request.document_type,

            "text":
                text,

            "html_preview":
                format_html_preview(text)
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                f"Document generation failed: "
                f"{exc}"
            )
        ) from exc


@router.post(
    "/export/txt",
    tags=["exports"]
)
def export_txt(request: ExportRequest):

    filename = (
        safe_filename(
            request.document_type
        )
        + ".txt"
    )

    return Response(
        format_txt(request.text),
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        }
    )


@router.post(
    "/export/docx",
    tags=["exports"]
)
def export_docx(request: ExportRequest):

    try:

        data = format_docx(
            request.text,
            request.document_type,
            request.terms,
            request.logo_base64
        )

        filename = (
            safe_filename(
                request.document_type
            )
            + ".docx"
        )

        return Response(
            data,
            media_type=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
            headers={
                "Content-Disposition":
                    f'attachment; filename="{filename}"'
            }
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"DOCX export failed: {exc}"
        ) from exc


@router.post(
    "/export/pdf",
    tags=["exports"]
)
def export_pdf(request: ExportRequest):

    try:

        data = format_pdf(
            request.text,
            request.document_type,
            request.terms,
            request.logo_base64
        )

        filename = (
            safe_filename(
                request.document_type
            )
            + ".pdf"
        )

        return Response(
            data,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    f'attachment; filename="{filename}"'
            }
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed: {exc}"
        ) from exc