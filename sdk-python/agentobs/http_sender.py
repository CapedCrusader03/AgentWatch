from typing import List, Optional
import requests
from agentobs.models import Span
from agentobs.tracer import clear_span_buffer


def send_spans_http(
    url: str = "http://localhost:8080/ingest",
    spans: Optional[List[Span]] = None,
    timeout: float = 5.0,
) -> bool:
    """POSTs current span buffer (or provided spans) as JSON to the given URL and clears the buffer.

    Returns True if request succeeded (200, 201, 202).
    """
    if spans is None:
        spans_to_send = clear_span_buffer()
    else:
        spans_to_send = spans

    if not spans_to_send:
        return True

    payload = [span.to_dict() for span in spans_to_send]
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.status_code in (200, 201, 202)
    except Exception as exc:
        raise RuntimeError(f"Failed to send spans to {url}: {exc}") from exc
