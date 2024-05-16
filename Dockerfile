FROM public.ecr.aws/docker/library/python:3.12.1-slim as base
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

FROM base as deps-resolver
RUN pip install pipenv
WORKDIR /app
COPY Pipfile* ./
RUN pipenv install --deploy

FROM base as runtime

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080 || exit 1

WORKDIR /app
RUN adduser --home /app --no-create-home --disabled-password --gecos '' --shell /bin/sh app
USER app
EXPOSE 8080
COPY --from=deps-resolver --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app app/ ./app
COPY --chown=app:app static/ ./static
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
