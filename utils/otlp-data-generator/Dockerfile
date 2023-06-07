FROM python:3.11-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install dependent libraries
ADD requirements.txt ./
RUN pip install -r requirements.txt

# add source code
ADD app.py utils.py ./

# apparently this instruments flask?
RUN opentelemetry-bootstrap -a install

ENV ENABLE_REQUEST_GENERATION=false
ENV FLASK_APP=otlpdatagen
ENV FLASK_RUN_PORT=8080
ENV LOG_LEVEL=info
ENV OTLP_ENDPOINT=collector:4317
ENV OTLP_LOG_ENDPOINT=collector:4317
ENV OTLP_METRIC_ENDPOINT=collector:4317
ENV OTLP_TRACE_ENDPOINT=collector:4317

# by default, we will use opentelemetry-instrument as an entrypoint
ENTRYPOINT ["opentelemetry-instrument"]

# and we will pass `flask run -p 8080` to it, which it will execute
CMD ["flask", "run"]