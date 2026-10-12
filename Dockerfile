# Cali Automation Project - Docker Setup
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers to a shared path so the non-root user can use them
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install --with-deps

# There is no display in the container, so run the browser headless
ENV HEADLESS=true

# Copy application files
COPY . .

# Create non-root user
RUN useradd -m -u 1000 cali && chown -R cali:cali /app
USER cali

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the API service (the same server used by goal_interface.html)
CMD ["python", "web_api.py"]
