
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse, JSONResponse
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.get("/")
async def root():
    return RedirectResponse(url="/v1/embeddings")


@app.post("/embeddings")
async def openai_embeddings(request: Request):
    body = await request.json()
    input_texts = body.get("input", [])
    model_name = body.get("model", "all-MiniLM-L6-v2")

    # Normalize input to a list
    if isinstance(input_texts, str):
        input_texts = [input_texts]

    embeddings = model.encode(input_texts)

    data = [
        {
            "object": "embedding",
            "embedding": emb.tolist(),
            "index": idx
        }
        for idx, emb in enumerate(embeddings)
    ]

    return JSONResponse(content={
        "object": "list",
        "data": data,
        "model": model_name,
        "usage": {"prompt_tokens": 0, "total_tokens": 0}
    })

@app.get("/other")
async def other():
    return {"message": "This is another route"}


@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()
    print(data)
    # Broadcast the data as a JSON string to all connected clients
    await manager.broadcast(json.dumps(data))
    return JSONResponse(content={"status": "data received and broadcasted"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("A client disconnected.")