from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

from passlib.context import CryptContext
from jose import jwt, JWTError

# 간단한 설정 — 실제 운영에서는 환경변수로 관리하세요.
SECRET_KEY = "change_this_secret_for_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pbkdf2_sha256 사용 (bcrypt에 의존하지 않음)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """pbkdf2_sha256으로 비밀번호 해시 (bcrypt 관련 문제 회피)"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해시 비교"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# Swagger UI에 전달할 oauth 초기값 (환경변수로 설정 권장)
SWAGGER_UI_PARAMS = {
    "persistAuthorization": True,
    "oauth": {
        "clientId": os.getenv("SWAGGER_CLIENT_ID", "your_client_id"),
        "clientSecret": os.getenv("SWAGGER_CLIENT_SECRET", "your_client_secret"),
        # 선택값: scope 등 추가 가능
        # "scopes": "openid profile email"
    },
}

def get_swagger_ui_params() -> dict:
    """메인에서 get_swagger_ui_html(..., swagger_ui_parameters=get_swagger_ui_params())처럼 사용"""
    return SWAGGER_UI_PARAMS
