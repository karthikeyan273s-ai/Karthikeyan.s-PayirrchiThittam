from backend.utils import (
    sanitize_text,
    terms_list,
    safe_filename
)


def test_sanitize_text():

    assert (
        sanitize_text(
            "A\u2013B\r\nC"
        )
        == "A-B\nC"
    )


def test_terms_list():

    assert terms_list(
        "A; B;; C"
    ) == [
        "A",
        "B",
        "C"
    ]


def test_safe_filename():

    assert safe_filename(
        "Lease Agreement / 2026"
    ) == "Lease_Agreement_2026"