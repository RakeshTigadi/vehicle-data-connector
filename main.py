from fastapi import FastAPI, Request
import uvicorn
import asyncio

app = FastAPI()

@app.post("/ingest")
async def ingest(request: Request):
    body = await request.json()
    vin = body.get("vin")
    speed = body.get("speed")
    timestamp = body.get("timestamp")

    await output.send({
        "vin": vin,
        "speed": speed,
        "timestamp": timestamp
    })

    return {"status": "ok"}

def start():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
