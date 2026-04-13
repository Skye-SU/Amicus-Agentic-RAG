FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt

COPY . .
RUN python -m compileall \
    server.py agent.py config.py data_loader.py hybrid_retriever.py quiz_generator.py \
    app.py rag_pipeline.py scripts tests

EXPOSE 7860

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
