FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache bash curl
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ /app/api/
COPY application/ /app/application/
COPY domain/ /app/domain/
COPY infrastructure/ /app/infrastructure/
COPY config/ /app/config/

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app
USER appuser

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
