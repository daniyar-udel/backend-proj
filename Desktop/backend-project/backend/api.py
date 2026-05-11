from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Message CRUD')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class MessageCreate(BaseModel):
    content: str

class MessageUpdate(BaseModel):
    content: str|None = None

class Message(BaseModel):
    id: int
    content: str

messages_db: list[Message] = [Message(id=0, content='First FastAPI message')]

def get_index(message_id) -> int:
    for i, val in enumerate(messages_db):
        if val.id == message_id:
            return i
    return -1

def create_id() -> int:
    return messages_db[-1].id + 1 if messages_db else 0

@app.get('/messages', response_model=list[Message])
async def read_messages() -> list[Message]:
    return messages_db

@app.get('/messages/{message_id}', response_model=Message)
async def reas_message(message_id: int) -> Message:
    idx = get_index(message_id)
    if idx == -1:
        raise HTTPException(status_code=404)
    return messages_db[idx]

@app.post('/messages', response_model=Message)
async def create_message(new_message: MessageCreate) -> Message:
    message = Message(id=create_id(), content=new_message.content)
    messages_db.append(message)
    return message

@app.put('/messages/{message_id}', response_model=Message)
async def put_message(message_id: int, put_message: MessageCreate) -> Message:
    idx = get_index(message_id)
    if idx == -1:
        raise HTTPException(status_code=404)
    message = Message(id=message_id, content=put_message.content)
    messages_db[idx] = message
    return message

@app.patch('/messages/{message_id}', response_model=Message)
async def update_message(message_id: int, payload: MessageUpdate) -> Message:
    idx = get_index(message_id)
    if idx == -1:
        raise HTTPException(status_code=404)
    if payload.content is not None:
        messages_db[idx].content = payload.content
    return messages_db[idx]

@app.delete('/messages/{message_id}')
async def delete_message(message_id: int):
    idx = get_index(message_id)
    if idx == -1:
        raise HTTPException(status_code=404)
    messages_db.pop(idx)
