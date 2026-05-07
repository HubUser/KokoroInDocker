FROM python:3.12

RUN apt-get update

# Create app directory
WORKDIR /usr/src/app

RUN pip install --upgrade pip

# Copy requirements file and install big dependencies
COPY requirements-base.txt ./
RUN pip install --no-cache-dir -r requirements-base.txt

# Copy requirements file and install smaller dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Create directory for audio output
RUN mkdir -p audio_output

# Set permissions for non-root user
RUN chmod -R 755 /usr/src/app

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["python", "server.py"]
