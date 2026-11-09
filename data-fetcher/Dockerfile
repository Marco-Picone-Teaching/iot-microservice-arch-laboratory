# Base image with Python 3.12 (Debian slim)
FROM python:3.12-slim

# Copy the uv binary from the official uv image (pinned version for reproducible builds)
COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /uvx /bin/

# Set the target container working directory to /app
WORKDIR /app

# uv settings: compile the bytecode at install time, use the Python of the image (no downloads)
# and print the application output without buffering
ENV UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1

# 1. Install only the dependencies, using the locked versions of uv.lock.
#    This layer is rebuilt only when pyproject.toml or uv.lock change, not when the source code changes
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

# 2. Copy the source code and the default configuration, then install the project itself
COPY src ./src
COPY fetcher_conf.yaml ./fetcher_conf.yaml
RUN uv sync --frozen --no-dev

# Use the virtual environment created by uv
ENV PATH="/app/.venv/bin:$PATH"

# Run the target application (command declared in pyproject.toml)
CMD ["mqtt-data-fetcher"]
