import databases
from sqlalchemy import create_engine, MetaData

from core.config import settings


engine = create_engine(settings.DATABASE_URL)
database = databases.Database(settings.DATABASE_URL)
metadata = MetaData()
