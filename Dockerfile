FROM python:3.14-alpine

# Without buffering, the output of print reaches the container log at once.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# The dependencies are installed in a separate layer, which only depends on requirements.txt.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY engine-service/ engine-service/

USER nobody

CMD ["python", "engine-service/engine_service.py"]
