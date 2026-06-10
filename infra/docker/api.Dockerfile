FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY openhip /app/openhip
COPY apps /app/apps
RUN pip install --upgrade pip && pip install -e ".[dev]"
EXPOSE 8000
