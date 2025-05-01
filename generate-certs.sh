#!/bin/bash

# Create directory for certificates
mkdir -p certs

# Generate self-signed certificates
openssl req -x509 -nodes -days 365 -new \
    -keyout certs/server.key -out certs/server.cert \
    -config ./openssl.cnf -extensions 'v3_ca'

echo "Self-signed certificates generated in certs/ directory"