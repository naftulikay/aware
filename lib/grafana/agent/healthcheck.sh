#!/usr/bin/env bash

set -euo pipefail

# while curl is not installed
while ! dpkg -s curl &>/dev/null ; do
  # apt-get update && apt-get install -y curl
  # the || is so that if it fails, it emits log messages as to *why* it failed
  DEBIAN_FRONTEND=noninteractive apt-get update &>/dev/null && \
    (DEBIAN_FRONTEND=noninteractive apt-get install -y curl &>/dev/null || \
     DEBIAN_FRONTEND=noninteractive apt-get install -y curl) || \
     sleep 2
done

# curl the admin interface
curl -s -f -o /dev/null http://127.0.0.1:12345/-/ready