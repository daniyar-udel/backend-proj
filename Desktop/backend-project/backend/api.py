from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class CreateBottle(BaseModel):
    name: str = Field(max_length=15)
    price: int = Field(ge=1)

class Bottle(CreateBottle):
    id: int

bottles_db: list[Bottle] = [Bottle(id=1, name='Deer Park', price=1)]

@app.get('/bottles', response_model=list[Bottle])
async def read_bottles() -> list[Bottle]:
    return bottles_db

@app.get('/bottles/{bottle_id}', response_model=Bottle)
async def read_bottle(bottle_id: int) -> Bottle:
    for bottle in bottles_db:
        if bottle.id == bottle_id:
            return bottle
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bottle not found')

@app.post('/bottles', response_model=Bottle)
async def create_bottle(new_bottle: CreateBottle) -> Bottle:
    next_id = len(bottles_db) + 1 if bottles_db else 0
    bottle = Bottle(id=next_id, name=new_bottle.name, price=new_bottle.price)
    bottles_db.append(bottle)
    return bottle

@app.put('/bottles/{bottle_id}', response_model=Bottle)
async def update_bottle(bottle_id:int, new_bottle: CreateBottle) -> Bottle:
    for i, bottle in enumerate(bottles_db):
        if bottle.id == bottle_id:
            update_bottle = Bottle(id=bottle_id, name=new_bottle.name, price=new_bottle.price)
            bottles_db[i] = update_bottle
            return update_bottle
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bottle not found')

@app.delete('/bottles/{bottle_id}', response_model=Bottle)
async def delete_bottle(bottle_id:int) -> Bottle:
    for i, bottle in enumerate(bottles_db):
        if bottle.id == bottle_id:
            bottles_db.pop(i)
            return bottle
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bottle not found')

@app.delete('/bottles', response_model=list[Bottle])
async def delete_bottles() -> list[Bottle]:
    bottles_db.clear()
    return bottles_db