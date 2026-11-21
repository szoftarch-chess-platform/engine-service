FROM python:3.14-slim

# Without buffering, the output of print reaches the container log at once.
ENV PYTHONUNBUFFERED=1
ENV STOCKFISH_PATH=/usr/games/stockfish

RUN apt-get update \
    && apt-get install -y --no-install-recommends stockfish \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# The dependencies are installed in a separate layer, which only depends on requirements.txt.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY engine_service/ engine_service/

USER nobody

CMD ["python", "-m", "engine_service.main"]
