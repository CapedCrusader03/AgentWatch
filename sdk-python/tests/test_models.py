import json
from agentobs.models import Span, TraceEvent


def test_span_to_json():
    span = Span(
        id="span-123",
        trace_id="trace-456",
        span_type="llm_call",
        name="test_llm",
        input="Hello world",
        output="Hi there!",
        started_at="2026-07-30T00:00:00Z",
        ended_at="2026-07-30T00:00:01Z",
        duration_ms=1000,
        tokens=15,
        cost=0.00003,
        metadata={"model": "gpt-4o"},
    )
    json_str = span.to_json()
    data = json.loads(json_str)

    expected_keys = {
        "id",
        "trace_id",
        "span_type",
        "name",
        "input",
        "output",
        "started_at",
        "ended_at",
        "duration_ms",
        "tokens",
        "cost",
        "metadata",
    }
    assert expected_keys.issubset(set(data.keys()))
    assert data["id"] == "span-123"
    assert data["trace_id"] == "trace-456"
    assert data["span_type"] == "llm_call"
    assert data["duration_ms"] == 1000
    assert data["tokens"] == 15


def test_trace_event_to_json():
    span = Span(trace_id="trace-789", name="test_tool")
    event = TraceEvent(trace_id="trace-789", event_type="span_completed", span=span)
    json_str = event.to_json()
    data = json.loads(json_str)

    assert "event_id" in data
    assert data["trace_id"] == "trace-789"
    assert data["span"]["name"] == "test_tool"
