FROM python:3.12.1-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base as deps-resolver
RUN pip install pipenv
WORKDIR /app
COPY Pipfile* ./
RUN pipenv install --deploy

FROM base as runtime
WORKDIR /app
RUN adduser --home /app --no-create-home --disabled-password --gecos '' --shell /bin/sh app
USER app
EXPOSE 8000
COPY --from=deps-resolver --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app app/ ./app
COPY --chown=app:app static/ ./static
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
