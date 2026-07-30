import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def current_iso_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Span:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    span_type: str = "tool_call"
    name: str = ""
    input: Optional[str] = None
    output: Optional[str] = None
    started_at: str = field(default_factory=current_iso_timestamp)
    ended_at: str = field(default_factory=current_iso_timestamp)
    duration_ms: int = 0
    tokens: int = 0
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class TraceEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    event_type: str = "span_created"
    timestamp: str = field(default_factory=current_iso_timestamp)
    span: Optional[Span] = None

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        if self.span is not None:
            res["span"] = self.span.to_dict()
        return res

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)
