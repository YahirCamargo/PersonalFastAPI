import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    token_id = Column(UUID, nullable=False, unique=True)
    token_hash = Column(String, nullable=False)
    expira_en = Column(DateTime,nullable=False)
    usado = Column(Boolean,nullable=False,default=False)
    usuarios_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )