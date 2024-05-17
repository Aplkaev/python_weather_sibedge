from fastapi import FastAPI
from datetime import datetime


from app.db.wetherModel import Weather, database
from app.waether import load_months


app = FastAPI()


@app.get("/")
async def read_root():
    return await Weather.objects.all()

@app.get("/date/{start_dt}/{end_dt}")
async def get_interval(start_dt: str, end_dt: str):
    # http://localhost:8008/date/2018-01-01/2018-02-15
    datetime_start = datetime.strptime(start_dt, '%Y-%m-%d')
    datetime_end = datetime.strptime(end_dt, '%Y-%m-%d')
    return await Weather.objects.filter(date__gte=datetime_start, date__lte=datetime_end).all()

@app.get("/date/{date}")
async def get_date(date: str):    
    # http://localhost:8008/date/2018-01-01
    return await Weather.objects.filter(date=datetime.strptime(date, '%Y-%m-%d')).all()

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

    count = await Weather.objects.count()
    if count == 0:
        await load_months()
    # await Weather.objects.get_or_create(date=current_dateTime, temperature=0)
