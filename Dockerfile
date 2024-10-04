# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev git && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global user.name "readme-bot"
RUN git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

RUN git config --global user.name "readme-bot"
RUN git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
# Install Poetry and project dependencies
RUN pip install uv && uv pip install -r pyproject.toml --system

# WORKDIR is overriden by Github Actions, so run full path
ENTRYPOINT ["uv", "run", "/app/src/main.py"]
