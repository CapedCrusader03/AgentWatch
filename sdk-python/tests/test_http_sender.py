import json
import pytest
import responses
from agentobs.http_sender import send_spans_http
from agentobs.tracer import start_span, end_span, get_span_buffer, reset_tracer


def setup_function():
    reset_tracer()


@responses.activate
def test_send_spans_http_success():
    target_url = "http://localhost:8080/ingest"
    responses.add(
        responses.POST,
        target_url,
        json={"status": "accepted"},
        status=202,
    )

    span = start_span("llm_query", span_type="llm_call", input="What is AI?")
    end_span(span.id, output="AI is artificial intelligence", tokens=20, cost=0.0002)

    assert len(get_span_buffer()) == 1

    success = send_spans_http(url=target_url)

    assert success is True
    assert len(get_span_buffer()) == 0  # Buffer cleared after sending

    assert len(responses.calls) == 1
    req = responses.calls[0].request
    assert req.url == target_url
    body = json.loads(req.body)
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["name"] == "llm_query"
    assert body[0]["tokens"] == 20


@responses.activate
def test_send_spans_http_failure():
    target_url = "http://localhost:8080/ingest"
    responses.add(
        responses.POST,
        target_url,
        status=500,
    )

    span = start_span("failing_tool", span_type="tool_call")
    end_span(span.id)

    with pytest.raises(RuntimeError, match="Failed to send spans"):
        send_spans_http(url=target_url)
