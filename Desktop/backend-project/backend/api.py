from fastapi import FastAPI

app = FastAPI()

@app.get('/mobile/{model}')
async def mobile(model: str) -> dict:
    return {'model': model}