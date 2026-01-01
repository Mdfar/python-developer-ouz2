from fastapi import FastAPI, BackgroundTasks from pydantic import BaseModel from typing import List, Any import uvicorn from pipelines.ingestion import KafkaProducerService

app = FastAPI(title="Kaarvi Data Platform API") producer = KafkaProducerService()

class DataPayload(BaseModel): source: str records: List[Any] schema_version: str

@app.post("/ingest/stream") async def ingest_stream(payload: DataPayload, background_tasks: BackgroundTasks): """ Entry point for real-time data ingestion. Validates schema and pushes to Kafka topic. """ background_tasks.add_task(producer.send_to_topic, payload.source, payload.records) return {"status": "accepted", "message": f"Processing {len(payload.records)} records from {payload.source}"}

@app.get("/health/pipelines") async def get_pipeline_health(): # Placeholder for monitoring logic return {"status": "healthy", "active_streams": 12, "latency_ms": 45}

if name == "main": uvicorn.run(app, host="0.0.0.0", port=8000)