# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev git && \
    rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

COPY . .

# Install Poetry and project dependencies
RUN pip install uv && \
    uv venv && \
    uv pip install -r pyproject.toml

ENTRYPOINT ["uv", "run", "src/main.py"]
