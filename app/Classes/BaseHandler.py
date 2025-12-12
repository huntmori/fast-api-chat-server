from typing import Optional

from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.Classes.ConnectionManager import ConnectionManager


class BaseHandler:
    @staticmethod
    async def handle(
            conn:"ConnectionManager",
            websocket: WebSocket,
            data: Optional[str] | dict,
            db: Session
    ):
        pass