import json
import os
import uuid
from typing import Dict, List, Optional

from sqlalchemy import JSON, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class UserRow(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    identifier: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), default="user")
    mode: Mapped[str] = mapped_column(String(20), default="P1_RETAIL")
    persona: Mapped[Dict] = mapped_column(JSON, default=dict)
    interests: Mapped[Dict] = mapped_column(JSON, default=dict)
    holdings: Mapped[List] = mapped_column(JSON, default=list)
    feedback: Mapped[List] = mapped_column(JSON, default=list)


class FeedzStore:
    def __init__(self, database_url: Optional[str] = None):
        url = database_url or os.getenv("DATABASE_URL") or "sqlite:///./feedz.db"
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        if os.getenv("APP_ENV", "development").lower() == "production":
            if not url.startswith("postgresql"):
                raise RuntimeError("Production requires DATABASE_URL pointing to PostgreSQL")
            if not os.getenv("AUTH_SECRET") or len(os.getenv("AUTH_SECRET", "")) < 32:
                raise RuntimeError("Production requires AUTH_SECRET with at least 32 characters")
        self.engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)

    def create_user(self, identifier: str, password_hash: str, name: str) -> Dict:
        identifier = identifier.strip().lower()
        with Session(self.engine) as session:
            existing = session.scalar(select(UserRow).where(UserRow.identifier == identifier))
            if existing:
                raise ValueError("A user with this identifier already exists")
            user = UserRow(
                id=str(uuid.uuid4()),
                identifier=identifier,
                password_hash=password_hash,
                name=name.strip(),
                mode="P1_RETAIL",
                persona={
                    "type": "Active investor",
                    "horizon": "Long term",
                    "style": "Deep analysis",
                    "alerts": "Daily digest",
                },
                interests={},
                holdings=[],
                feedback=[],
            )
            session.add(user)
            session.commit()
            return self._public_user(user)

    def get_by_identifier(self, identifier: str) -> Optional[Dict]:
        with Session(self.engine) as session:
            user = session.scalar(select(UserRow).where(UserRow.identifier == identifier.strip().lower()))
            return self._public_user(user, include_password=True) if user else None

    def get_user(self, user_id: str) -> Optional[Dict]:
        with Session(self.engine) as session:
            user = session.get(UserRow, user_id)
            return self._public_user(user) if user else None

    def save_profile(self, user_id: str, profile: Dict) -> Dict:
        with Session(self.engine) as session:
            user = session.get(UserRow, user_id)
            if not user:
                raise KeyError("User not found")
            user.name = profile["name"]
            user.mode = profile["mode"]
            user.persona = profile["persona"]
            user.interests = profile["interests"]
            user.holdings = profile["holdings"]
            session.commit()
            return self._public_user(user)

    def save_holdings(self, user_id: str, holdings: List[Dict]) -> Dict:
        with Session(self.engine) as session:
            user = session.get(UserRow, user_id)
            if not user:
                raise KeyError("User not found")
            user.holdings = holdings
            session.commit()
            return self._public_user(user)

    def append_feedback(self, user_id: str, feedback: Dict) -> int:
        with Session(self.engine) as session:
            user = session.get(UserRow, user_id)
            if not user:
                raise KeyError("User not found")
            entries = list(user.feedback or [])
            entries.append(feedback)
            user.feedback = entries
            session.commit()
            return len(entries)

    def healthcheck(self) -> bool:
        with self.engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return True

    @staticmethod
    def _public_user(user: UserRow, include_password: bool = False) -> Dict:
        result = {
            "user_id": user.id,
            "identifier": user.identifier,
            "name": user.name,
            "role": user.role,
            "mode": user.mode,
            "persona": dict(user.persona or {}),
            "interests": dict(user.interests or {}),
            "holdings": list(user.holdings or []),
        }
        if include_password:
            result["password_hash"] = user.password_hash
        return result
