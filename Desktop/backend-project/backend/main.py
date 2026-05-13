from fastapi import FastAPI, Depends, HTTPException
from starlette import status

async def pagination_route_func(page: int):
    if page == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if page < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

app = FastAPI(dependencies=[Depends(pagination_route_func)])
    
async def pagination_def_func(limit: int, page: int) -> list:
    return [{'limit': limit, 'page': page}]

@app.get('/messages')
async def messages(pagination: dict=Depends(pagination_def_func)) -> dict:
    return {'messages': pagination}