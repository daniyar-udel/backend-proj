from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CreatPhone(BaseModel):
    model: str
    price: int

class Phones(BaseModel):
    id: int
    model: str
    price: int

phones_db: list[Phones] = [Phones(id=1, model='Galaxy A8', price=500)]

@app.get('/phones', response_model=list[Phones])
async def read_phones() -> list[Phones]:
    return phones_db

@app.get('/phones/{phone_id}', response_model=Phones)
async def read_phone(phone_id:int) -> Phones:
    for phone in phones_db:
        if phone.id == phone_id:
            return phone
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no phone')

@app.post('/phones', response_model=Phones, status_code=status.HTTP_201_CREATED)
async def create_phone(new_phone: CreatPhone) -> Phones:
    curr_id = phones_db[-1].id + 1 if phones_db else 0
    phone = Phones(id=curr_id, model=new_phone.model, price=new_phone.price)
    phones_db.append(phone)
    return phone

@app.put('/phones/{phone_id}', response_model=Phones, status_code=status.HTTP_200_OK)
async def change_phone(phone_id:int, new_phone: CreatPhone) -> Phones:
    for i, phone in enumerate(phones_db):
        if phone.id == phone_id:
            phone = Phones(id=phone_id, model=new_phone.model, price=new_phone.price)
            phones_db[i] = phone
            return phone
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no phone')
        
@app.delete('/phones/{phone_id}', response_model=Phones, status_code=status.HTTP_200_OK)
async def delete_phone(phone_id: int) -> Phones:
    for i, phone in enumerate(phones_db):
        if phone.id == phone_id:
            phones_db.pop(i)
            return phone
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no phone')

@app.delete('/phones', response_model=list[Phones])
async def delete_phones() -> list[Phones]:
    phones_db.clear()
    return phones_db

    