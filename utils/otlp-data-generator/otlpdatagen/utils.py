#!/usr/bin/env python3.11

from opentelemetry import trace, metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import Meter, MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import Tracer, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import logfmter
import logging
import os


APP_NAME = "oteldatagen"

DEFAULT_LOG_LEVEL = "debug"
DEFAULT_OTLP_ENDPOINT = "localhost:4317"

ENV_VAR_LOG_LEVEL = "LOG_LEVEL"
ENV_VAR_OTLP_ENDPOINT = "OTLP_ENDPOINT"
ENV_VAR_OTLP_LOG_ENDPOINT = "OTLP_LOG_ENDPOINT"
ENV_VAR_OTLP_METRIC_ENDPOINT = "OTLP_METRIC_ENDPOINT"
ENV_VAR_OTLP_TRACING_ENDPOINT = "OTLP_TRACE_ENDPOINT"
ENV_VAR_ENABLE_REQUEST_GENERATION = "ENABLE_REQUEST_GENERATION"

OTLP_RESOURCE = Resource(attributes={
    SERVICE_NAME: APP_NAME,
})


class Telemetry(object):

    def __init__(self, logger: logging.Logger, tracer: Tracer, meter: Meter):
        self.logger, self.tracer, self.meter = logger, tracer, meter


def configure_telemetry():
    """Configure all telemetry systems: logging, tracing, and metrics."""
    return Telemetry(logger=configure_logging(), tracer=configure_tracing(), meter=configure_metrics())


def configure_logging() -> logging.Logger:
    """Configure logging."""
    # first, configure otlp logging
    otlp_logger_provider = LoggerProvider(resource=OTLP_RESOURCE)
    otlp_logger_provider.add_log_record_processor(BatchLogRecordProcessor(
        exporter=OTLPLogExporter(endpoint=get_otlp_logging_endpoint(), insecure=True)))

    set_logger_provider(otlp_logger_provider)

    otlp_logging_handler = LoggingHandler(level=logging.NOTSET, logger_provider=otlp_logger_provider)
    logging.getLogger().addHandler(otlp_logging_handler)

    # next, configure console logging with logfmter
    logfmter_formatter = logfmter.Logfmter()

    console_logging_handler = logging.StreamHandler()
    console_logging_handler.setFormatter(logfmter_formatter)
    logging.getLogger().addHandler(console_logging_handler)

    # finally, configure level
    level_name = os.environ.get(ENV_VAR_LOG_LEVEL, DEFAULT_LOG_LEVEL).upper()
    level = logging.getLevelNamesMapping().get(level_name)

    if level is None:
        raise Exception(f"Unable to configure log level, unrecognized level: {level_name}")

    logger = logging.getLogger().getChild(APP_NAME)

    return logger


def configure_tracing():
    """Configure tracing."""
    trace_provider = TracerProvider(resource=OTLP_RESOURCE)
    trace_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=get_otlp_tracing_endpoint(), insecure=True))
    trace_provider.add_span_processor(trace_processor)
    trace.set_tracer_provider(trace_provider)

    return trace.get_tracer(f"{APP_NAME}.tracer")


def configure_metrics() -> Meter:
    """Configure metrics."""
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=get_otlp_metrics_endpoint(), insecure=True))
    metric_provider = MeterProvider(resource=OTLP_RESOURCE, metric_readers=[metric_reader])
    metrics.set_meter_provider(metric_provider)

    return metrics.get_meter(f"{APP_NAME}.meter")


def get_otlp_logging_endpoint(default_endpoint=DEFAULT_OTLP_ENDPOINT) -> str:
    """Returns the OTLP logging endpoint from the environment or the default, localhost:4317"""
    return os.environ.get(ENV_VAR_OTLP_LOG_ENDPOINT, os.environ.get(ENV_VAR_OTLP_ENDPOINT, DEFAULT_OTLP_ENDPOINT))


def get_otlp_metrics_endpoint(default_endpoint=DEFAULT_OTLP_ENDPOINT) -> str:
    """Returns the OTLP metrics endpoint from the environment or the default, localhost:4317."""
    return os.environ.get(ENV_VAR_OTLP_METRIC_ENDPOINT, os.environ.get(ENV_VAR_OTLP_ENDPOINT, DEFAULT_OTLP_ENDPOINT))


def get_otlp_tracing_endpoint(default_endpoint=DEFAULT_OTLP_ENDPOINT) -> str:
    """Returns the OTLP tracing endpoint from the environment or the default, localhost:4317."""
    return os.environ.get(ENV_VAR_OTLP_TRACING_ENDPOINT, os.environ.get(ENV_VAR_OTLP_ENDPOINT, DEFAULT_OTLP_ENDPOINT))


def is_request_generation_enabled() -> bool:
    """Indicates whether automatic request generation is enabled."""
    return os.environ.get(ENV_VAR_ENABLE_REQUEST_GENERATION, "false").lower().strip() in ["true", "on", "yes", "y",
                                                                                          "enabled"]
