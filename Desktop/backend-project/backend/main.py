from starlette.requests import Request
from fastapi import Depends, FastAPI

async def first_func(request: Request) -> str:
    return request.method

async def second_func(method: str=Depends(first_func)) -> str:
    return method

app = FastAPI()

@app.get('/test')
async def third_func(method_type: str=Depends(second_func)) -> str:
    return method_type