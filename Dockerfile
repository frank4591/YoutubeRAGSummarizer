FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY youtube_app ./youtube_app
COPY main.py ./main.py

RUN pip install --upgrade pip \
    && pip install .

EXPOSE 7860

CMD ["python", "main.py"]
