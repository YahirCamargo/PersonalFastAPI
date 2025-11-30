from sqlalchemy import Column, DateTime,ForeignKey,String
from sqlalchemy.dialects.mysql import SMALLINT, BOOLEAN
from db.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(SMALLINT(unsigned=True), nullable=False,autoincrement=True,primary_key=True)
    token = Column(String(255),nullable=False,unique=True)
    expira_en = Column(DateTime, nullable=False)
    usado = Column(BOOLEAN,nullable=False, default=0)
    usuarios_id = Column(
        SMALLINT(unsigned=True),
        ForeignKey("usuarios.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )



"""
CREATE TABLE refresh_tokens (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    token VARCHAR(255) NOT NULL UNIQUE,
    expira_en DATETIME NOT NULL,
    usado BOOLEAN NOT NULL DEFAULT 0,
    usuarios_id SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=INNODB;
"""