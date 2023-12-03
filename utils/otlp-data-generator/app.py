#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from opentelemetry import trace, metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from flask import Flask

from random import SystemRandom
from time import sleep

import logging
import os

random = SystemRandom()


APP_NAME = "oteldatagen"


OTLP_LOG_ENDPOINT = os.environ.get("OTLP_LOG_ENDPOINT", os.environ.get("OTLP_ENDPOINT", "localhost:4317"))
OTLP_METRIC_ENDPOINT = os.environ.get("OTLP_METRIC_ENDPOINT", os.environ.get("OTLP_ENDPOINT", "localhost:4317"))
OTLP_TRACE_ENDPOINT = os.environ.get("OTLP_TRACE_ENDPOINT", os.environ.get("OTLP_ENDPOINT", "localhost:4317"))

print(f"logs={OTLP_LOG_ENDPOINT}, metrics={OTLP_METRIC_ENDPOINT}, traces={OTLP_TRACE_ENDPOINT}")


resource = Resource(attributes={
    SERVICE_NAME: APP_NAME,
})

# setup OTLP log exporter
logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter=OTLPLogExporter(endpoint=OTLP_LOG_ENDPOINT,
                                                                                          insecure=True)))
set_logger_provider(logger_provider)

logging_handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logging.getLogger().addHandler(logging_handler)

console_handler = logging.StreamHandler()
logging.getLogger().addHandler(console_handler)

# setup OTLP metric exporter
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=OTLP_METRIC_ENDPOINT, insecure=True))
metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metric_provider)

# setup OTLP trace exporter
trace_provider = TracerProvider(resource=resource)
trace_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_TRACE_ENDPOINT, insecure=True))
trace_provider.add_span_processor(trace_processor)
trace.set_tracer_provider(trace_provider)

# get the tracer and meter for our application
tracer, meter = (trace.get_tracer(f"{APP_NAME}.tracer"), metrics.get_meter(f"{APP_NAME}.meter"))

# create a counter for keeping track of all the rolls
roll_counter = meter.create_counter('roll_counter', description="The number of rolls by roll value.")

# create a logger to be used by our whole app
app_logger = logging.getLogger().getChild(APP_NAME)

app = Flask(__name__)


@app.route("/")
def index():
    # start a span
    with tracer.start_as_current_span("roll") as span:
        logger = app_logger.getChild('index')

        roll: int = randroll()

        if roll == 1:
            logger.debug("Snake eyes")
        elif roll == 2:
            logger.debug("Double or nothing")
        elif roll == 3:
            logger.info("It's getting interesting")
        elif roll == 4:
            logger.warning("Oh jeez here we go")
        else:
            logger.error("It's an error, Bob")

        # set an attribute on the span
        span.set_attribute("roll.value", roll)

        # record the roll
        roll_counter.add(1, {"roll.value": roll})

        # return the result
        return f"YOUR ROLL IS {roll}"


def randroll() -> int:
    with tracer.start_as_current_span("randroll") as span:
        logger = app_logger.getChild('randroll')

        sleep_millis = random.randint(1, 50)

        # sleep
        logger.debug("Sleeping for %d milliseconds", sleep_millis)

        sleep(sleep_millis * 0.001)

        span.set_attribute("sleep.millis", sleep_millis)

        return random.randint(1, 6)


@app.route("/health")
def healthcheck():
    return 200

