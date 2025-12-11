import json

from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

import logging

from app import dtos

from app.Classes.ConnectionManager import ConnectionManager
from app.database import get_db

router = APIRouter(prefix="/ws/chat", tags=["Chat"])

manager = ConnectionManager()

logger = logging.getLogger(__name__)

@router.websocket(path='', name='Chat')
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            data = json.loads(text)

            type: str = data.get("type")
            payload = data.get("payload")
            logger.info(f"Received message of type {type}")

            if type == "ws_headers":
                await manager.logIn(websocket, payload.get('access_token'), db)
            elif type == "room.create":
                await manager.room_create(websocket, data, db)
                pass
            elif type == "room.join":
                pass
            elif type == "room.leave":
                pass
            elif type == "room.chat":
                pass
            elif type == "room.list":
                pass
            elif type == "room.delete":
                pass
            else:
                await manager.send_personal_message(text,websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{websocket.client.host} left the chat")