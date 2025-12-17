from datetime import datetime
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
def registro_de_voluntario(voluntario: VoluntariosRequest, db: Session = Depends(get_db)):


    voluntario_atual = db.query(VoluntariosModel).filter_by(email=voluntario.email).first()
    if voluntario_atual:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="esse email ja esta cadastrado")

    novo_voluntario = VoluntariosModel(
        nome=voluntario.nome,
        email=voluntario.email,
        telefone=voluntario.telefone,
        cargo_pretendido=voluntario.cargo_pretendido,
        disponibilidade=voluntario.disponibilidade,
        status=StatusEnum.ATIVO,
        criado_em=datetime.now()
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

    voluntario_atual = db.query(VoluntariosModel).get(id_voluntario)

    if voluntario_atual is None:
        raise HTTPException(status_code=404, detail="item não encontrado")

    return VoluntariosResponse(
        id=voluntario_atual.id,
        nome=voluntario_atual.nome,
        email=voluntario_atual.email,
        telefone=voluntario_atual.telefone,
        cargo_pretendido=voluntario_atual.cargo_pretendido,
        disponibilidade=voluntario_atual.disponibilidade,
        status=voluntario_atual.status,
        criado_em=voluntario_atual.criado_em
    )


@router.put("/{id_voluntario}", status_code=status.HTTP_200_OK)
def atualizar_voluntario(id_voluntario: int, voluntario: VoluntariosRequest, db: Session = Depends(get_db)) ->VoluntariosResponse:

    voluntario_atual = db.query(VoluntariosModel).get(id_voluntario)

    if voluntario_atual is None:
        raise HTTPException(status_code=404, detail="item não encontrado")

    voluntario_atual.nome = voluntario.nome
    voluntario_atual.email = voluntario.email
    voluntario_atual.telefone = voluntario.telefone
    voluntario_atual.cargo_pretendido = voluntario.cargo_pretendido
    voluntario_atual.disponibilidade = voluntario.disponibilidade

    db.add(voluntario_atual)
    db.commit()
    db.refresh(voluntario_atual)

    return VoluntariosResponse(
        id=voluntario_atual.id,
        nome=voluntario_atual.nome,
        email=voluntario_atual.email,
        telefone=voluntario_atual.telefone,
        cargo_pretendido=voluntario_atual.cargo_pretendido,
        disponibilidade=voluntario_atual.disponibilidade,
        status=voluntario_atual.status,
        criado_em=voluntario_atual.criado_em
    )

@router.delete("/{id_voluntario}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_voluntario(id_voluntario: int, db: Session = Depends(get_db)) -> None:

    voluntario_atual = db.query(VoluntariosModel).get(id_voluntario)

    if voluntario_atual is None:
        raise HTTPException(status_code=404, detail="item não encontrado")

    voluntario_atual.status = StatusEnum.INATIVO
    db.add(voluntario_atual)
    db.commit()
    db.refresh(voluntario_atual)

    return None

