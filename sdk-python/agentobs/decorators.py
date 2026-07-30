import functools
import inspect
from typing import Any, Callable, Optional

from agentobs.tracer import start_span, end_span


def traceable(
    _func: Optional[Callable] = None,
    *,
    span_type: str = "tool_call",
    name: Optional[str] = None,
) -> Callable:
    """Decorator to trace function execution automatically as spans.

    Usage:
        @traceable
        def my_func(): ...

        @traceable(span_type="llm_call", name="custom_name")
        def call_llm(): ...
    """

    def decorator(func: Callable) -> Callable:
        span_name = name or func.__name__

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                input_str = f"args={args}, kwargs={kwargs}" if (args or kwargs) else None
                span = start_span(name=span_name, span_type=span_type, input=input_str)
                try:
                    result = await func(*args, **kwargs)
                    output_str = str(result) if result is not None else None
                    end_span(span.id, output=output_str)
                    return result
                except Exception as exc:
                    end_span(span.id, error=str(exc))
                    raise

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                input_str = f"args={args}, kwargs={kwargs}" if (args or kwargs) else None
                span = start_span(name=span_name, span_type=span_type, input=input_str)
                try:
                    result = func(*args, **kwargs)
                    output_str = str(result) if result is not None else None
                    end_span(span.id, output=output_str)
                    return result
                except Exception as exc:
                    end_span(span.id, error=str(exc))
                    raise

            return sync_wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
