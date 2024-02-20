import uvicorn
from fastapi import FastAPI

from src.app.campaigns.views import router as campaigns_router
from src.app.clients.views import router as clients_router
from src.app.messages.views import router as messages_router

app = FastAPI(title="Mailing manager")


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(clients_router, prefix="/clients")
app.include_router(campaigns_router, prefix="/campaigns")
app.include_router(messages_router, prefix="/messages")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
