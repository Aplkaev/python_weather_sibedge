import ormar
import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base

from ..db.config import settings

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
metadata.create_all(engine)