# python
import logging

from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from typing import Optional, TYPE_CHECKING

from app.Classes.BaseHandler import BaseHandler

if TYPE_CHECKING:
    from app.Classes.ConnectionManager import ConnectionManager

from app.auth import decode_access_token
from app.models import User

logger = logging.getLogger(__name__)

class LoginHandler(BaseHandler):
    @staticmethod
    async def handle(
            conn:"ConnectionManager",
            websocket: WebSocket,
            data: Optional[str],
            db: Session
    ):
        logger.info(f"logIn : data ={data}")

        if not data:
            await conn.send_error(websocket, "No data provided")
            return

        # 토큰 복호화 및 사용자명 추출
        try:
            decoded = decode_access_token(data)
        except Exception as e:
            await conn.send_error(websocket, "Invalid data")
            return

        # decode_access_data이 문자열(예: username) 또는 dict(payload)를 반환할 수 있으므로 안전하게 처리
        user_name: Optional[str] = None
        if isinstance(decoded, str):
            user_name = decoded
        elif isinstance(decoded, dict):
            # 표준적으로 'sub' 또는 'username' 키 사용 가능성 처리
            user_name = decoded.get("sub") or decoded.get("username") or decoded.get("user")
        else:
            user_name = None

        logger.info(f"user_name : {user_name}")

        if not user_name:
            await conn.send_error(websocket, "Invalid data payload")
            return

        try:
            user = db.query(User).filter(User.username == user_name).first()
            if not user:
                await conn.send_error(websocket, "Invalid data or user not found")
                return

            # 안전한 사용자 식별자 추출 (uid, id, username 순)
            uid = getattr(user, "uid", None)
            if uid is None:
                await conn.send_error(websocket, "user has no usable identifier")
                return

            # 로그인 연결 저장
            conn.set_user_socket(uid, websocket)

            # 직렬화 가능한 사용자 정보만 전송
            user_info = {
                "uid": uid,
                "username": getattr(user, "username", None),
                "email": getattr(user, "email", None),
                # 필요한 추가 필드만 담음
            }
            await conn.send_success(websocket, user_info)
        except Exception as e:
            logger.exception(e)
            await conn.send_error(websocket, "Internal server error during logIn")
            return