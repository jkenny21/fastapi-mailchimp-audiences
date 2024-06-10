import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from pydantic_core import MultiHostUrl

load_dotenv()

POSTGRES_USER           = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD       = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB             = os.environ.get("POSTGRES_DB")
POSTGRES_SERVER         = os.environ.get("POSTGRES_SERVER")
POSTGRES_PORT           = int( os.environ.get("POSTGRES_PORT") )

SQLMODEL_DATABASE_URI = str( MultiHostUrl.build(
                            scheme   = "postgresql+psycopg",
                            username = POSTGRES_USER,
                            password = POSTGRES_PASSWORD,
                            host     = POSTGRES_SERVER,
                            port     = POSTGRES_PORT,
                            path     = POSTGRES_DB,
                        ) )


engine = create_engine(SQLMODEL_DATABASE_URI)

async def create_tables():
    SQLModel.metadata.create_all(engine)