#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from flask import Flask, request

from random import SystemRandom
from threading import Thread
from time import sleep

from .utils import configure_telemetry

import os
import requests
import sys
import time
import uuid

random = SystemRandom()


# setup telemetry
telemetry = configure_telemetry()
app_logger = telemetry.logger
meter = telemetry.meter
tracer = telemetry.tracer

app_logger.error("SHEEYIT")


# create a counter for keeping track of all the rolls
roll_counter = meter.create_counter('roll_counter', description="The number of rolls by roll value.")

app = Flask(utils.APP_NAME)


# @app.before_request
# def before_request():
#     request.headers["X-Request-Id"] = str(uuid.uuid4())


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


def generate_requests():
    """Automatically generate requests to the service repeatedly."""
    # attempt to get from CLI
    port = None

    for index, arg in enumerate(sys.argv[1:]):
        if arg in ['-p', '--port']:
            port = int(sys.argv[index + 2])
            break

    if port is None:
        env_port = os.environ.get('FLASK_RUN_PORT')

        if env_port is not None:
            port = int(env_port)

    if port is None:
        server_name = app.config.get('SERVER_NAME')

        if server_name is not None:
            port = int(server_name.split(':')[-1])

    if port is None:
        port = 5000

    while True:
        # _resp = requests.get(f"http://localhost:{port}/")
        time.sleep(2.0)


if utils.is_request_generation_enabled():
    Thread(name="request-generator", target=generate_requests).run()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
