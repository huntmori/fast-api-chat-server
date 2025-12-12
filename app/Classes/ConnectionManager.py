import json
import logging
from typing import Dict, Optional

from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from app.Classes.LoginHandler import LoginHandler
from app.Classes.RoomCreateHandler import RoomCreateHandler
from app.dtos import BaseResponse
from app.payloads.RoomCreate import RoomCreate

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        # 키는 사용자 식별자(uid 또는 id 또는 username)로 저장
        self.log_in_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        logger.info("websocket header : %s", websocket.headers)
        logger.info("websocket cookies : %s", websocket.cookies)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, recipient: WebSocket):
        await recipient.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def send_error(websocket: WebSocket, error: str):
        logger.error(error)
        await websocket.send_text(json.dumps(BaseResponse.error(error)))

    @staticmethod
    async def send_success(websocket: WebSocket, data):
        await websocket.send_text(json.dumps(BaseResponse.success("", data)))

    def get_user_uid_by_websockets(self, websocket: WebSocket) -> str:
        uid = next(
            (k for k,v in self.log_in_connections.items() if v == websocket), None
        )
        logger.info(f"test : uid = {uid}")
        return uid

    def set_user_socket(self, uid, websocket):
        self.log_in_connections[uid] = websocket
        logger.info(f"setUserSocket : uid = {uid}")
        logger.info(f"connections : {self.log_in_connections}")
        pass

    async def login(self, websocket: WebSocket, token: Optional[str], db: Session):
        await LoginHandler.handle(self, websocket, token, db)

    async def room_create(self, websocket: WebSocket, data: dict, db: Session):
        RoomCreateHandler.handle(self, websocket, data, db)
        pass