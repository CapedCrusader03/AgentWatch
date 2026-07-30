-- Migration: 0001_init.sql
-- Description: Create spans table for storing agent execution spans

CREATE TABLE IF NOT EXISTS spans (
    id VARCHAR(64) PRIMARY KEY,
    trace_id VARCHAR(64) NOT NULL,
    span_type VARCHAR(32) NOT NULL,
    name VARCHAR(255) NOT NULL,
    input TEXT,
    output TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ NOT NULL,
    duration_ms BIGINT NOT NULL,
    tokens INT DEFAULT 0,
    cost NUMERIC(10, 6) DEFAULT 0.000000,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_spans_trace_id ON spans (trace_id);
CREATE INDEX IF NOT EXISTS idx_spans_started_at ON spans (started_at DESC);
