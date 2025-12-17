from datetime import datetime, UTC
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from voluntários.models.dto import VoluntariosResponse, VoluntariosRequest, StatusEnum

from shared.dependencies import get_db

from voluntários.models.voluntario_models import VoluntariosModel

router = APIRouter(prefix="/voluntario")


@router.get("/", response_model=List[VoluntariosResponse] ,status_code=status.HTTP_200_OK)
def lista_de_usuarios(status: str = None, cargo : str = None, disponibilidade: str = None, db: Session = Depends(get_db)) -> List[VoluntariosResponse]:
    if not status is None:
        return db.query(VoluntariosModel).filter_by(status=status).all()
    elif not cargo is None:
        return db.query(VoluntariosModel).filter_by(cargo_pretendido=cargo).all()
    elif not disponibilidade is None:
        return db.query(VoluntariosModel).filter_by(disponibilidade=disponibilidade).all()
    else:
        return db.query(VoluntariosModel).all()

@router.post("/",status_code=status.HTTP_201_CREATED)
def novo_voluntario(voluntario: VoluntariosRequest, db: Session = Depends(get_db)):

    current_voluntario = db.query(VoluntariosModel).filter_by(email=voluntario.email).first()
    if current_voluntario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="esse email ja esta cadastrado")

    novo_voluntario = VoluntariosModel(
        nome=voluntario.nome,
        email=voluntario.email,
        telefone=voluntario.telefone,
        cargo_pretendido=voluntario.cargo_pretendido,
        disponibilidade=voluntario.disponibilidade,
        status=StatusEnum.ATIVO,
        criado_em=datetime.now(UTC)
    )
    db.add(novo_voluntario)
    db.commit()
    db.refresh(novo_voluntario)

    return VoluntariosResponse(
        id=novo_voluntario.id,
        nome=novo_voluntario.nome,
        email=novo_voluntario.email,
        telefone=novo_voluntario.telefone,
        cargo_pretendido=novo_voluntario.cargo_pretendido,
        disponibilidade=voluntario.disponibilidade,
        status=novo_voluntario.status,
        criado_em=novo_voluntario.criado_em
    )

@router.get("/{id_voluntario}", response_model=VoluntariosResponse, status_code=status.HTTP_200_OK)
def buscar_voluntario(id_voluntario: str, db: Session = Depends(get_db)):

    current_voluntario = db.query(VoluntariosModel).get(id_voluntario)

    if current_voluntario is None:
        raise HTTPException(status_code=404, detail="item não encontrado")

    return VoluntariosResponse(
        id=current_voluntario.id,
        nome=current_voluntario.nome,
        email=current_voluntario.email,
        telefone=current_voluntario.telefone,
        cargo_pretendido=current_voluntario.cargo_pretendido,
        disponibilidade=current_voluntario.disponibilidade,
        status=current_voluntario.status,
        criado_em=current_voluntario.criado_em
    )


@router.put("/{id_voluntario}", status_code=status.HTTP_200_OK)
def atualizar_voluntario(id_voluntario: int, voluntario: VoluntariosRequest, db: Session = Depends(get_db)) ->VoluntariosResponse:

    current_voluntario = db.query(VoluntariosModel).get(id_voluntario)

    if current_voluntario is None:
        raise HTTPException(status_code=404, detail="item não encontrado")

    current_voluntario.nome = voluntario.nome
    current_voluntario.email = voluntario.email
    current_voluntario.telefone = voluntario.telefone
    current_voluntario.cargo_pretendido = voluntario.cargo_pretendido
    current_voluntario.disponibilidade = voluntario.disponibilidade

    db.add(current_voluntario)
    db.commit()
    db.refresh(current_voluntario)

    return VoluntariosResponse(
        id=current_voluntario.id,
        nome=current_voluntario.nome,
        email=current_voluntario.email,
        telefone=current_voluntario.telefone,
        cargo_pretendido=current_voluntario.cargo_pretendido,
        disponibilidade=current_voluntario.disponibilidade,
        status=current_voluntario.status,
        criado_em=current_voluntario.criado_em
    )

@router.delete("/{id_voluntario}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_voluntario(id_voluntario: int, db: Session = Depends(get_db)) -> None:

    current_voluntario = db.query(VoluntariosModel).get(id_voluntario)

    if current_voluntario is None:
        raise HTTPException(status_code=404, detail="item não encontrado")

    current_voluntario.status = StatusEnum.INATIVO
    db.add(current_voluntario)
    db.commit()
    db.refresh(current_voluntario)

    return None

