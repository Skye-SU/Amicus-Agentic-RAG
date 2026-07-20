"""
Legacy Streamlit entry point.

Amicus now runs through the FastAPI backend in server.py and the static
frontend under static/. This file stays in the repository only so old links or
commands fail gently instead of exposing a second, stale application surface.
"""

from __future__ import annotations

MESSAGE = """
Amicus no longer uses the legacy Streamlit app.

Run the supported FastAPI application instead:

    uvicorn server:app --host 0.0.0.0 --port 7860

Then open http://127.0.0.1:7860.
""".strip()


def main() -> None:
    print(MESSAGE)


if __name__ == "__main__":
    main()
