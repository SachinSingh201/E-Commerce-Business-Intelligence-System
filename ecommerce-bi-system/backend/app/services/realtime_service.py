import asyncio
import json
from ..core.database import SessionLocal
from .kpi_service import KPIService

async def broadcast_kpi_updates(manager):
    """
    Background task to periodically fetch KPIs and broadcast to all connected WebSocket clients.
    """
    while True:
        try:
            db = SessionLocal()
            try:
                kpis = KPIService.get_kpi_summary(db)
                # We can also add a timestamp to let the client know when it was updated
                message = {
                    "type": "kpi_update",
                    "data": kpis
                }
                await manager.broadcast(json.dumps(message))
            finally:
                db.close()
        except Exception as e:
            print(f"Error in broadcast_kpi_updates: {e}")
        
        # Broadcast every 10 seconds
        await asyncio.sleep(10)
