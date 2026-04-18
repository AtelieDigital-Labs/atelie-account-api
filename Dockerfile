FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY services/account/pyproject.toml services/account/uv.lock ./

RUN uv sync --no-editable

ENV PATH="/app/.venv/bin:$PATH"

COPY services/account /app/

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]