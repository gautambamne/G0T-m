FROM python:3.12-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Install dependencies
# Copy pyproject.toml and uv.lock first to leverage cache
COPY pyproject.toml uv.lock ./
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies using uv
RUN /bin/uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Install the project itself
RUN /bin/uv sync --frozen --no-dev

# Set the PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose port (optional, good practice)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
