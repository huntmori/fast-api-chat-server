import sys
import os

# 현재 디렉토리를 모듈 검색 경로에 추가 (필요 시)
sys.path.append(os.getcwd())

from app.database import engine, Base
# 모델을 import해야 Base.metadata에 테이블 정보가 등록됩니다.
from app.models import User 

def init_db():
    print(f"Database URL: {engine.url}")
    print("Creating database tables based on entities...")
    try:
        # 여기에 정의된 모든 모델을 기반으로 테이블을 생성합니다.
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
