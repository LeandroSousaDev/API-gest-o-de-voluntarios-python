from enum import Enum

from pydantic import BaseModel


class VoluntariosResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    cargo_pretendido: str
    disponibilidade: str
    status: str

class VoluntariosRequest(BaseModel):
    nome: str
    email: str
    telefone: str
    cargo_pretendido: CargoEnum
    disponibilidade: DisponibilidadeEnum

class DisponibilidadeEnum(str, Enum):
    MANHA = "manha"
    TARDE = "tarde"
    INTEGRAL = "integral"

class StatusEnum(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"

class CargoEnum(str, Enum):
    TRAINEE = "trainee"
    GERENTE = "gerente"
    DIRETOR = "diretor"
    PRESIDENTE = "presidente"
