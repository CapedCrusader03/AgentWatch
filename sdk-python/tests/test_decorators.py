import pytest
from agentobs.decorators import traceable
from agentobs.tracer import get_span_buffer, reset_tracer


def setup_function():
    reset_tracer()


def test_traceable_success():
    @traceable(span_type="tool_call", name="multiply_numbers")
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(3, 4)
    assert result == 12

    buffer = get_span_buffer()
    assert len(buffer) == 1

    span = buffer[0]
    assert span.name == "multiply_numbers"
    assert span.span_type == "tool_call"
    assert span.output == "12"
    assert span.duration_ms >= 0


def test_traceable_exception():
    @traceable(span_type="llm_call")
    def failing_function():
        raise ValueError("Invalid prompt format")

    with pytest.raises(ValueError, match="Invalid prompt format"):
        failing_function()

    buffer = get_span_buffer()
    assert len(buffer) == 1

    span = buffer[0]
    assert span.name == "failing_function"
    assert span.span_type == "error"
    assert span.metadata["error"] == "Invalid prompt format"


def test_traceable_bare_decorator():
    @traceable
    def simple_add(x, y):
        return x + y

    assert simple_add(5, 5) == 10
    buffer = get_span_buffer()
    assert len(buffer) == 1
    assert buffer[0].name == "simple_add"
    assert buffer[0].span_type == "tool_call"
