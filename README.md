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

## Usage

After starting the compose environment, you can now send OpenTelemetry logs, metrics, and traces to localhost, port 4317
for HTTP/2 and gRPC, port 4318 for HTTP/1.

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