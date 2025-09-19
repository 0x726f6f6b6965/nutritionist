# syntax=docker/dockerfile:1.4

FROM --platform=linux/amd64 python:3.13-slim
# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY /app /service/app
COPY pyproject.toml /service
COPY .python-version /service
COPY uv.lock /service


# Install the application dependencies.
WORKDIR /service
RUN uv venv --system-site-packages
RUN uv sync --frozen --no-cache

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run the application.
CMD ["/service/.venv/bin/fastapi", "run", "/service/app/main.py", "--port", "8080", "--host", "0.0.0.0"]