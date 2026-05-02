country_dict = {
    'Russia': ['Moscow', 'St. Petersburg', 'Novosibirsk', 'Ekaterinburg', 'Kazan'],
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia'],}

from fastapi import FastAPI

app = FastAPI()

@app.get('/country/{country}')
async def list_cities(country:str, limit:int) -> dict:
    return {'country': country, 'cities': country_dict[country][0: limit]}