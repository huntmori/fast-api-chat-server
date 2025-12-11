# FastAPI JWT Authentication Project

FastAPI 프로젝트 with JWT 인증, MariaDB, SQLAlchemy 2.0

## 기능

- ✅ FastAPI 웹 프레임워크
- ✅ JWT 토큰 기반 인증/인가
- ✅ MariaDB 데이터베이스 (Docker Compose)
- ✅ SQLAlchemy 2.0 ORM
- ✅ Pydantic v2 데이터 검증
- ✅ 비밀번호 해싱 (bcrypt)
- ✅ CORS 미들웨어

## 프로젝트 구조

```
fast-api-practice/
├── app/
│   ├── __init__.py
│   ├── database.py          # 데이터베이스 연결 및 세션
│   ├── models.py            # SQLAlchemy 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── auth.py              # JWT 인증 로직
│   ├── dependencies.py      # FastAPI 의존성
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # 인증 엔드포인트
│       └── users.py         # 사용자 엔드포인트
├── main.py                  # FastAPI 앱 진입점
├── requirements.txt         # Python 의존성
├── docker-compose.yml       # MariaDB 컨테이너 설정
├── .env                     # 환경 변수
└── .gitignore
```

## 설치 및 실행

### 1. 가상환경 활성화 및 의존성 설치

```powershell
# 가상환경 활성화 (이미 생성되어 있음)
.\fastapienv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2. MariaDB 컨테이너 시작

```powershell
docker-compose up -d
```

### 3. FastAPI 서버 실행

```powershell
python main.py
```

또는

```powershell
uvicorn main:app --reload
```
또는
```powershell
python -m uvicorn main:app --reload
```

## API 엔드포인트

### 인증 (Authentication)

- `POST /api/auth/register` - 새 사용자 등록
- `POST /api/auth/login` - 로그인 (JWT 토큰 발급)
- `POST /api/auth/token` - OAuth2 호환 로그인 (Swagger UI용)

### 사용자 (Users)

- `GET /api/users/me` - 현재 사용자 정보 조회
- `PUT /api/users/me` - 현재 사용자 정보 수정
- `DELETE /api/users/me` - 현재 사용자 계정 삭제
- `GET /api/users/` - 모든 사용자 목록 조회
- `GET /api/users/{user_id}` - 특정 사용자 정보 조회

### 기타

- `GET /` - 루트 엔드포인트
- `GET /health` - 헬스 체크

## API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 사용 예시

### 1. 사용자 등록

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### 2. 로그인

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. 인증된 요청

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 환경 변수

`.env` 파일에서 다음 환경 변수를 설정할 수 있습니다:

```env
DATABASE_URL=mysql+pymysql://fastapi_user:fastapi_password@localhost:3306/fastapi_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 데이터베이스

### MariaDB 연결 정보

- Host: localhost
- Port: 3306
- Database: fastapi_db
- User: fastapi_user
- Password: fastapi_password
- Root Password: rootpassword

### 데이터베이스 테이블

`users` 테이블이 자동으로 생성됩니다:

- id (INT, PRIMARY KEY)
- email (VARCHAR, UNIQUE)
- username (VARCHAR, UNIQUE)
- hashed_password (VARCHAR)
- is_active (BOOLEAN)
- is_superuser (BOOLEAN)
- created_at (DATETIME)
- updated_at (DATETIME)

## 보안 사항

⚠️ **프로덕션 환경에서는 반드시:**

1. `.env` 파일의 `SECRET_KEY`를 안전한 랜덤 문자열로 변경
2. CORS 설정을 적절히 제한
3. 데이터베이스 비밀번호 변경
4. HTTPS 사용

## 기술 스택

- **FastAPI** 0.122.0 - 현대적인 고성능 웹 프레임워크
- **SQLAlchemy** 2.0.36 - SQL 툴킷 및 ORM
- **Pydantic** 2.12.5 - 데이터 검증 및 설정
- **PyMySQL** - MariaDB/MySQL 드라이버
- **python-jose** - JWT 토큰 생성/검증
- **passlib** - 비밀번호 해싱
- **Uvicorn** - ASGI 서버
- **MariaDB** 11.6 - 데이터베이스

## 라이선스

MIT

