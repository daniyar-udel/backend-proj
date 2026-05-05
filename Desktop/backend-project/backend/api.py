from fastapi import FastAPI, Query
from typing import Annotated

profiles_dict = {
    'alex': {'name': 'Александр', 'age': 33, 'phone': '+79463456789', 'email': 'alex@my-site.com'},
}

app = FastAPI()

@app.get('/users')
async def retrieve_user_profile(username: Annotated[str | None,
                                                   Query(min_length=2, max_length=50,
                                                        description='Имя пользователя')] = None):
    if username in profiles_dict:
        return profiles_dict[username]
    return {'message': f'Пользователь {username} не найден.'}