from sqlmodel import SQLModel, create_engine
from app.config import settings

engine = create_engine( str( settings.SQLMODEL_DATABASE_URI ) )

async def create_tables():
    SQLModel.metadata.create_all(engine)