#!/bin/bash

podman container stop kokoro_tts-api_1
podman container rm kokoro_tts-api_1
fuser -k 3000/tcp
podman-compose up --build