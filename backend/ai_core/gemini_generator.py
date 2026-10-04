from backend.config import settings
from backend.utils import sanitize_text, terms_list


class GeminiDocumentGenerator:

    def __init__(self):

        self.client = None

        if (
            settings.gemini_api_key
            and not settings.demo_mode
        ):
            from google import genai

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def _demo_document(
        self,
        document_type,
        parties,
        terms,
        dates,
        language
    ):

        party_lines = [
            p.strip()
            for p in parties.replace(",", ";").split(";")
            if p.strip()
        ]

        term_lines = terms_list(terms)

        if language.lower().startswith("tamil"):

            return (
                f"{document_type.upper()}\n\n"
                f"Effective Date: {dates}\n\n"
                "PARTIES\n"
                + "; ".join(party_lines)
                + "\n\n"
                "AGREEMENT\n"
                "This is a demonstration draft generated "
                "by LegalEase. It records the supplied "
                "terms and requires legal review before use.\n\n"
                "KEY TERMS\n"
                + "\n".join(
                    f"- {x}" for x in term_lines
                )
                + "\n\n"
                "SIGNATURES\n"
                "Party 1: ____________________\n"
                "Party 2: ____________________\n"
            )

        return (
            f"{document_type.upper()}\n\n"
            f"Effective Date: {dates}\n\n"

            "PARTIES\n"

            + "\n".join(
                f"- {p}" for p in party_lines
            )

            + "\n\n"

            "TERMS AND CONDITIONS\n"

            + "\n".join(
                f"{i}. {x}"
                for i, x in enumerate(
                    term_lines,
                    1
                )
            )

            + "\n\n"

            "GENERAL PROVISIONS\n"

            "This AI-assisted draft must be adapted "
            "to the applicable jurisdiction and "
            "reviewed by a qualified legal professional "
            "before signing or use.\n\n"

            "SIGNATURES\n"

            "Party 1: ____________________    "
            "Date: __________\n"

            "Party 2: ____________________    "
            "Date: __________\n\n"

            "LEGAL REVIEW NOTICE: This AI-assisted "
            "draft is for informational and drafting "
            "purposes only and should be reviewed by "
            "a qualified legal professional before "
            "signing or use."
        )

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates,
        language="English",
        tone="Formal and professional"
    ):

        if (
            settings.demo_mode
            or not self.client
        ):

            return self._demo_document(
                document_type,
                parties,
                terms,
                dates,
                language
            )

        from google.genai import types

        prompt = f"""
You are the drafting engine for LegalEase,
an AI-assisted legal document generator.

Create a complete, structured legal document draft.

Document type:
{document_type}

Parties and roles:
{parties}

Effective date:
{dates}

User terms:
{terms}

Language:
{language}

Tone:
{tone}

Rules:

1. Use ONLY facts supplied by the user.

2. Never invent names, dates, amounts,
addresses, laws, jurisdictions,
registration numbers, or material facts.

3. Preserve the meaning of the supplied terms.

4. Use a professional structure.

5. Include:
- Title
- Parties
- Background where useful
- Numbered clauses
- General provisions
- Signature blocks

6. If jurisdiction is not supplied,
do not claim compliance with a particular
jurisdiction.

7. Do not provide a legal opinion.

8. Do not claim that the document is
legally enforceable.

9. Use [INSERT ...] placeholders for
necessary missing information.

10. Return plain text only.

11. Do not use Markdown code fences.

12. End with a legal-review notice.

Generate the complete document now.
"""

        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt.strip(),
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=12000
            )
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return sanitize_text(text)