import asyncio
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import dashboard, sales, forecasting, customers
from .core.config import settings
from .services.realtime_service import broadcast_kpi_updates

app = FastAPI(title=settings.PROJECT_NAME)

# Connection Manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def library_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Handle stale connections
                pass

manager = ConnectionManager()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to launch background tasks
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_kpi_updates(manager))

# WebSocket endpoint
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.library_connect(websocket)
    try:
        while True:
            # Keep connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Include routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])
app.include_router(forecasting.router, prefix="/api/forecast", tags=["Forecasting"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce BI System API"}
