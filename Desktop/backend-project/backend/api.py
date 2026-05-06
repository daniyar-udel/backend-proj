from fastapi import FastAPI, status, HTTPException, Body

app = FastAPI()

car_db = {0: 'Lexus ct 200h'}

@app.get('/cars')
async def read_cars() -> dict:
    return car_db

@app.get('/cars/{cars_id}')
async def read_cars_id(cars_id: int) -> str:
    try:
        return car_db[cars_id]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, description='Car not found')
    
@app.post('/cars', status_code=status.HTTP_201_CREATED)
async def create_car(car: str = Body()) -> str:
    curr_ind = max(car_db) + 1 if car_db else 0
    car_db[curr_ind] = car
    return 'Car created'

@app.put('/cars/{car_id}', status_code=status.HTTP_200_OK)
async def update_car(car_id: int, car: str = Body()) -> str:
    if car_id not in car_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    car_db[car_id] = car
    return 'Car updated'

@app.delete('/cars/{car_id}', status_code=status.HTTP_200_OK)
async def delete_car(car_id: int) -> str:
    if car_id not in car_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    car_db.pop(car_id)
    return f'Car with {car_id} id deleted'

@app.delete('/cars')
async def delete_cars() -> str:
    car_db.clear()
    return 'Car data cleared'