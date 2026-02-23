# Base image from official Open WebUI
FROM ghcr.io/open-webui/open-webui:main

# Install Python dependencies for tools
RUN pip install --no-cache-dir \
    httpx \
    pymupdf

# Create tools directory
RUN mkdir -p /app/backend/data/tools

# Copy custom tools
COPY tools/ /app/backend/data/tools/

# Set working directory
WORKDIR /app/backend

# Expose port
EXPOSE 8080

# Use the default entrypoint from the base image
