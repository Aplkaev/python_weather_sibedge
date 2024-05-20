from fastapi import FastAPI
from datetime import datetime


from app.db.WetherModel import Weather, database
from app.weather import load_months

app = FastAPI()


@app.get("/date/{start_dt}/{end_dt}")
async def get_interval(start_dt: datetime, end_dt: datetime):
    # http://localhost:8008/date/2018-01-01/2018-02-15
    # datetime_start = datetime.strptime(start_dt, '%Y-%m-%d')
    # datetime_end = datetime.strptime(end_dt, '%Y-%m-%d')
    return await Weather.objects.filter(
        date__gte=start_dt,
        date__lte=end_dt).all()


@app.get("/date/{date}")
async def get_date(date: datetime):
    # http://localhost:8008/date/2018-01-01
    return await Weather.objects.filter(
        date=datetime.strptime(date, '%Y-%m-%d')
    ).all()
    return await Weather.objects.filter(date=date).all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    count = await Weather.objects.count()
    if count == 0:
        await load_months()
