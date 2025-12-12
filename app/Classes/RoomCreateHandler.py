from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from app.Classes.BaseHandler import BaseHandler
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.Classes.ConnectionManager import ConnectionManager


class RoomCreateHandler(BaseHandler):
    @staticmethod
    def handle(
            conn:"ConnectionManager",
            websocket: WebSocket,
            data: Optional[str] | dict,
            db: Session
    ):
        pass