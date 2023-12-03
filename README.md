# aware

A Docker Compose environment with a full [OpenTelemetry][opentelemetry] stack for collecting, storing, and analyzing log
data, metrics, and traces.

[Jaeger][jaeger] is used for storing traces, [Loki][loki] is used for storing logs, [Prometheus][prometheus] is used as
a time-series database for storing metrics, the [OpenTelemetry Collector][collector] is used for
ingesting/transforming/storing data in the relevant backends, and [Grafana][grafana] is used as the web UI for accessing
logs/traces/metrics. 

## Getting Started

Obviously, you'll need [Docker][docker] and [Docker Compose][compose], once these are installed, everything can be
brought online with a single command:

```shell
docker compose up
```

And that's it!

If you'd like to run the OTLP data generator utility, add the `generator` profile when running the cluster and allow
building of the local image:

```shell
docker compose --profile generator up --build
```

## Usage

After starting the compose environment, there are a few provided ways to send telemetry data to the collector:

<dl>
 <dt>OpenTelemetry</dt>
 <dd>
  You can send OpenTelemetry logs, metrics, and traces to localhost on port 4317 for a gRPC transport and port 4318
  for an HTTP/1 transport.
 </dd>
 <dt>GELF</dt>
 <dd>You can send log data over UDP to localhost on port 12201 in GELF format.</dd>
 <dt>Syslog</dt>
 <dd>You can send RFC-5424 format syslog messages to localhost on port 5514 via both TCP and UDP.</dd>
</dl>

To access your observability data, open [http://localhost:3000](http://localhost:3000) to access Grafana.

## License

Licensed at your discretion under either:

 - [Apache Software License, Version 2.0](./LICENSE-APACHE)
 - [MIT License](./LICENSE-MIT)

 [compose]: https://docs.docker.com/compose/
 [docker]: https://www.docker.com/community/open-source/
 [opentelemetry]: https://opentelemetry.io
 [jaeger]: https://jaegertracing.io
 [loki]: https://grafana.com/oss/loki/
 [prometheus]: https://prometheus.io
 [collector]: https://opentelemetry.io/docs/collector/
 [grafana]: https://grafana.com/oss/grafana/