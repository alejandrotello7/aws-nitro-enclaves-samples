#!/bin/bash
# Forwards traffic from VSOCK port 6000 to local TCP port 6000
socat vsock-listen:6000,reuseaddr,fork tcp-connect:127.0.0.1:6000 &
