import uvicorn
from fastapi import FastAPI

from shared.database import Base, engine
from voluntários.routers import voluntarios_routers

from voluntários.models import voluntario_models
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(voluntarios_routers.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/busca")
def query_teste(teste: str = None, teste2: str = None):
    if not teste is None:
        return "teste existe"
    elif not teste2 is None:
        return "teste2 existe "
    else:
        return "não passou parametro"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
