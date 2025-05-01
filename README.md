# Text-to-Speech API Server

A containerized HTTPS server that provides a text-to-speech API endpoint using Podman.

## Features

- HTTPS server with self-signed certificates
- Text-to-speech conversion via API
- Podman containerization for easy deployment

## Prerequisites

- Podman and Podman Compose

## Getting Started

1. Clone this repository
2. Generate SSL certificates (for development only):
   ```
   chmod +x generate-certs.sh
   ./generate-certs.sh
   ```
3. Build and start the container:
   ```
   podman-compose up --build
   ```
4. The server will be available at `https://localhost:3000`

## API Usage

Send a POST request to `/api/tts` with JSON payload:

```json
{
  "text": "This is the text that will be converted to speech",
  "speed": 1.0
}
```

The response will be an audio file (WAV format) of the synthesized speech.

Example using curl:
```bash
curl -k -X POST \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, this is a test of the text to speech API", "speed": 1.0}' \
  -o speech.wav \
  https://localhost:3000/api/tts
```

Note: The `-k` flag is needed to skip certificate validation when using self-signed certificates.

## Production Use

For production environments, replace the self-signed certificates with valid SSL certificates by:

1. Placing your certificates in the `certs/` directory
2. Or setting the environment variables `SSL_KEY_PATH` and `SSL_CERT_PATH` to point to your certificates

## Related project

Check out [Vocalize](https://github.com/HubUser/Vocalize) Chrome extension that uses this solution to convert select browser text to speech.

Generated self-signed certificates need to be imported to **Trusted Root Certification Authorities** with `certmgr.msc` service. To make this API usable with [Vocalize](https://github.com/HubUser/Vocalize) extension.
