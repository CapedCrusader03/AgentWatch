import sys
import time
from agentobs import (
    clear_span_buffer,
    get_current_trace_id,
    get_span_buffer,
    send_spans_http,
    set_current_trace_id,
    traceable,
)


@traceable(span_type="llm_call", name="generate_agent_plan")
def fake_llm_call(prompt: str) -> str:
    print(f"  [LLM] Generating plan for: '{prompt}'")
    time.sleep(0.05)
    return "1. Search web for weather. 2. Calculate temperature difference."


@traceable(span_type="tool_call", name="search_web_tool")
def fake_tool_call(query: str) -> str:
    print(f"  [Tool] Executing web search: '{query}'")
    time.sleep(0.02)
    return "Current temperature in San Francisco: 65F, Tokyo: 78F"


@traceable(span_type="tool_call", name="calculator_tool")
def fake_calculator(expression: str) -> str:
    print(f"  [Tool] Running calculator: '{expression}'")
    time.sleep(0.01)
    return "Temperature difference is 13 degrees Fahrenheit."


def main():
    trace_id = "trace-demo-001"
    set_current_trace_id(trace_id)
    print(f"=== Starting Instrumented Agent Run (Trace ID: {trace_id}) ===")

    # Execute simulated agent workflow
    plan = fake_llm_call("Compare temperature between SF and Tokyo")
    print(f"  [Agent Output] Plan: {plan}")

    search_res = fake_tool_call("weather in SF and Tokyo")
    print(f"  [Agent Output] Search: {search_res}")

    calc_res = fake_calculator("78 - 65")
    print(f"  [Agent Output] Calc: {calc_res}")

    # Inspect captured spans
    spans = get_span_buffer()
    print(f"\n=== Captured {len(spans)} Spans in Buffer ===")
    for idx, span in enumerate(spans, 1):
        print(
            f"  Span #{idx}: ID={span.id} | Name={span.name:<20} | Type={span.span_type:<10} | Duration={span.duration_ms}ms"
        )

    # Attempt to POST spans to ingestion service HTTP endpoint
    ingest_url = "http://localhost:8080/ingest"
    print(f"\nAttempting HTTP POST to ingestion service at {ingest_url}...")
    try:
        send_spans_http(url=ingest_url)
        print("Successfully POSTed spans to ingestion service!")
    except Exception as exc:
        print(f"HTTP POST failed as expected (Ingestion service not running yet): {exc}")


if __name__ == "__main__":
    main()
