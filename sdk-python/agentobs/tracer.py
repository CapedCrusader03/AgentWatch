import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from agentobs.models import Span, current_iso_timestamp

# In-memory storage for active spans (in-flight) and completed span buffer
_active_spans: Dict[str, Tuple[Span, float]] = {}
_span_buffer: List[Span] = []
_current_trace_id: Optional[str] = None


def get_current_trace_id() -> str:
    global _current_trace_id
    if not _current_trace_id:
        _current_trace_id = str(uuid.uuid4())
    return _current_trace_id


def set_current_trace_id(trace_id: str) -> None:
    global _current_trace_id
    _current_trace_id = trace_id


def reset_tracer() -> None:
    global _current_trace_id
    _active_spans.clear()
    _span_buffer.clear()
    _current_trace_id = None


def get_span_buffer() -> List[Span]:
    return list(_span_buffer)


def clear_span_buffer() -> List[Span]:
    global _span_buffer
    buffer = list(_span_buffer)
    _span_buffer.clear()
    return buffer


def start_span(
    name: str,
    span_type: str = "tool_call",
    trace_id: Optional[str] = None,
    input: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Span:
    effective_trace_id = trace_id or get_current_trace_id()
    now_perf = time.perf_counter()
    start_time_iso = current_iso_timestamp()

    span = Span(
        id=str(uuid.uuid4()),
        trace_id=effective_trace_id,
        span_type=span_type,
        name=name,
        input=input,
        started_at=start_time_iso,
        metadata=dict(metadata) if metadata else {},
    )
    _active_spans[span.id] = (span, now_perf)
    return span


def end_span(
    span_id: str,
    output: Optional[str] = None,
    error: Optional[str] = None,
    tokens: int = 0,
    cost: float = 0.0,
) -> Optional[Span]:
    if span_id not in _active_spans:
        return None

    span, start_perf = _active_spans.pop(span_id)
    end_perf = time.perf_counter()
    end_time_iso = current_iso_timestamp()

    duration_ms = max(1, int((end_perf - start_perf) * 1000))

    span.ended_at = end_time_iso
    span.duration_ms = duration_ms
    span.output = output
    span.tokens = tokens
    span.cost = cost

    if error:
        span.metadata["error"] = error
        if span.span_type != "error":
            span.metadata["original_span_type"] = span.span_type
            span.span_type = "error"

    _span_buffer.append(span)
    return span
