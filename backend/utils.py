import html
import re


def sanitize_text(text: str) -> str:

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
        "\u2026": "..."
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return re.sub(
        r"[ \t]+\n",
        "\n",
        text
    ).strip()


def escape_html(text: str) -> str:
    return html.escape(
        text,
        quote=True
    )


def terms_list(terms: str) -> list[str]:

    return [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]


def safe_filename(value: str) -> str:

    value = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        value.strip()
    )

    value = value.strip("_")[:80]

    return value or "legal_document"