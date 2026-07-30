import time
from agentobs.tracer import (
    start_span,
    end_span,
    get_span_buffer,
    clear_span_buffer,
    reset_tracer,
    get_current_trace_id,
    set_current_trace_id,
)


def setup_function():
    reset_tracer()


def test_start_and_end_span():
    set_current_trace_id("test-trace-101")
    span = start_span(name="search_db", span_type="tool_call", input="query=agents")

    assert span.id is not None
    assert span.trace_id == "test-trace-101"
    assert span.name == "search_db"
    assert len(get_span_buffer()) == 0

    time.sleep(0.01)  # sleep 10ms to ensure duration_ms > 0

    completed_span = end_span(span.id, output="found 5 results", tokens=25, cost=0.001)

    assert completed_span is not None
    assert completed_span.duration_ms > 0
    assert completed_span.output == "found 5 results"
    assert completed_span.tokens == 25
    assert completed_span.cost == 0.001

    buffer = get_span_buffer()
    assert len(buffer) == 1
    assert buffer[0].id == span.id


def test_span_with_error():
    span = start_span(name="api_request", span_type="llm_call")
    completed_span = end_span(span.id, error="404 Not Found")

    assert completed_span is not None
    assert completed_span.span_type == "error"
    assert completed_span.metadata["error"] == "404 Not Found"

    buffer = clear_span_buffer()
    assert len(buffer) == 1
    assert len(get_span_buffer()) == 0
