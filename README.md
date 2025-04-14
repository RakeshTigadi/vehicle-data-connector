# Vehicle Data Connector

A FastAPI-based connector to ingest real-time vehicle data (vin, speed, timestamp) into Condense pipelines.

## POST /ingest

Example Payload:
```json
{
  "vin": "VIN001",
  "speed": 65.4,
  "timestamp": "2025-04-14T17:45:00Z"
}
