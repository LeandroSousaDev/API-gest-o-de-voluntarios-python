from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from shared.database import Base

class VoluntariosModel(Base):
    __tablename__ = "voluntarios"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100) ,nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(100), nullable=False)
    cargo_pretendido: Mapped[str] = mapped_column(String(100), nullable=False)
    disponibilidade: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=False)