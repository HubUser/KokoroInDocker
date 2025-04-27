#!/bin/bash

# Create directory for certificates
mkdir -p certs

# Generate self-signed certificates
openssl req -nodes -new -x509 \
  -keyout certs/server.key \
  -out certs/server.cert \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost" \
  -days 365
  
echo "Self-signed certificates generated in certs/ directory" 