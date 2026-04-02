FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv
ENV PATH="/uvbin:${PATH}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

RUN chmod +x entrypoint.sh
EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
