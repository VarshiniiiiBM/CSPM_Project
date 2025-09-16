from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import FileResponse
import asyncio

app = FastAPI()
clients = set()

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except:
        clients.remove(ws)

async def broadcast(data: dict):
    living = set()
    for ws in clients:
        try:
            await ws.send_json(data)
            living.add(ws)
        except:
            pass
    clients.clear()
    clients.update(living)

@app.post("/ingest")
async def ingest(request: Request):
    data = await request.json()
    asyncio.create_task(broadcast(data))
    return {"status": "ok"}
