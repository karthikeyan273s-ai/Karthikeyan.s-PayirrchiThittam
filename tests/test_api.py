from fastapi.testclient import TestClient

from backend.main import app
from backend.config import settings


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()[
        "status"
    ] == "ok"


def test_generate_demo(
    monkeypatch
):

    monkeypatch.setattr(
        settings,
        "demo_mode",
        True
    )

    monkeypatch.setattr(
        settings,
        "gemini_api_key",
        ""
    )

    response = client.post(

        "/generate",

        json={

            "document_type":
                "NDA",

            "parties":
                "Alice (Discloser); "
                "Bob (Recipient)",

            "terms":
                "Confidentiality; "
                "Return information within 10 days",

            "dates":
                "October 2, 2026"
        }
    )

    assert response.status_code == 200

    assert "NDA" in (
        response.json()["text"]
    )