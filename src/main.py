import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Mailing manager")


@app.get("/")
async def root():
    return {"message": "Hello"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
