FROM python:3.10

# Install espeak (text-to-speech engine)
RUN apt-get update && apt-get install -y espeak

# Create app directory
WORKDIR /usr/src/app

# Copy requirements file and install big dependencies
COPY requirements-base.txt ./
RUN pip install --no-cache-dir -r requirements-base.txt

# Copy requirements file and install smaller dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Create directory for certificates if they don't exist
RUN mkdir -p certs

# If certs don't exist in the source, generate them
RUN if [ ! -f certs/server.key ] || [ ! -f certs/server.cert ]; then \
    apt-get install -y openssl && \
    openssl req -nodes -new -x509 \
    -keyout certs/server.key \
    -out certs/server.cert \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost" \
    -days 365; \
  fi

# Create directory for audio output
RUN mkdir -p audio_output

# Set permissions for non-root user
RUN chmod -R 755 /usr/src/app

# # Create a non-root user and switch to it
# RUN chown -R node:node /usr/src/app
# USER node

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["python", "server.py"] 