FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reliable python package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency specifications
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen || uv pip install --system -r <(uv pip compile pyproject.toml)

# Copy application source code
COPY config/ ./config/
COPY src/ ./src/
COPY dashboard/ ./dashboard/
COPY Makefile ./

EXPOSE 8008 8501

CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8008"]
