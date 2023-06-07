# otlp-data-generator

A simple Flask application which emits logging, tracing, and metrics data to an OpenTelemetry endpoint.

## Configuration

The following environment variables are utilized by the application:

<dl>
    <dt><code>ENABLE_REQUEST_GENERATION</code></dt>
    <dd>
        <p>Whether the application should automatically generate HTTP requests to itself. This is useful to force
           data generation without manually making requests to the service.</p>
        <p>Default: <code>false</code></p>
    </dd>
    <dt><code>LOG_LEVEL</code></dt>
    <dd>
        <p>The log level for the application logger.</p>
        <p>Default: <code>info</code></p>
    </dd>
    <dt><code>OTLP_ENDPOINT</code></dt>
    <dd>
        <p>A hostname and port combination to be used as the default OpenTelemetry endpoint.</p>
        <p>Default: <code>localhost:4317</code></p>
    </dd>
    <dt><code>OTLP_LOG_ENDPOINT</code></dt>
    <dd>
        <p>A hostname and port combination to be used for shipping OpenTelemetry log data.</p>
        <p>Default: value of the <code>OTLP_ENDPOINT</code> variable.</p>
    </dd>
    <dt><code>OTLP_METRIC_ENDPOINT</code></dt>
    <dd>
        <p>A hostname and port combination to be used for shipping OpenTelemetry metric data.</p>
        <p>Default: value of the <code>OTLP_ENDPOINT</code> variable.</p>
    </dd>
    <dt><code>OTLP_TRACE_ENDPOINT</code></dt>
    <dd>
        <p>A hostname and port combination to be used for shipping OpenTelemetry trace data.</p>
        <p>Default: value of the <code>OTLP_ENDPOINT</code> variable.</p>
    </dd>
</dl>