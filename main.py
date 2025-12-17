import uvicorn
from fastapi import FastAPI

from shared.database import Base, engine
from voluntários.routers import voluntarios_routers

from voluntários.models import voluntario_models
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(voluntarios_routers.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
