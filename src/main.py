import uvicorn
from fastapi import FastAPI

from src.app.clients.views import router as clients_router

app = FastAPI(title="Mailing manager")


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(clients_router, prefix="/clients")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
