import ormar
import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base

from ..db.config import settings
# from .BaseMeta import BaseMeta, metadata
DATABASE_URL = "postgresql://fastapi_traefik:fastapi_traefik@db:5432/fastapi_traefik"

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()
Base = declarative_base()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
    
class Weather(ormar.Model):
    class Meta(BaseMeta):
        tablename = "weather"

    id: int = ormar.Integer(primary_key=True)
    date: str = ormar.Date(nullable=False)
    temperature: int = ormar.Integer(nullable=False)

engine = sqlalchemy.create_engine(settings.db_url)
# metadata.drop_all(engine)
metadata.create_all(engine)
# Base.metadata.create_all(engine)
# Weather = Weather(date="2018-01-01", temperature=1, completed=False)
# Weather.save()
