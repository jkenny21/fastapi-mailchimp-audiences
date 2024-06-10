# import os
# from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv()

# LIST_ID = os.environ.get("MAILCHIMP_AUDIENCE_ID")
# MAILCHIMP_API_KEY       = os.environ.get("MAILCHIMP_API_KEY")
# MAILCHIMP_SERVER_PREFIX = os.environ.get("MAILCHIMP_SERVER_PREFIX")
# POSTGRES_USER           = os.environ.get("POSTGRES_USER")
# POSTGRES_PASSWORD       = os.environ.get("POSTGRES_PASSWORD")
# POSTGRES_DB             = os.environ.get("POSTGRES_DB")
# POSTGRES_SERVER         = os.environ.get("POSTGRES_SERVER")
# POSTGRES_PORT           = int( os.environ.get("POSTGRES_PORT") )

# SQLMODEL_DATABASE_URI = str( MultiHostUrl.build(
#                             scheme   = "postgresql+psycopg",
#                             username = POSTGRES_USER,
#                             password = POSTGRES_PASSWORD,
#                             host     = POSTGRES_SERVER,
#                             port     = POSTGRES_PORT,
#                             path     = POSTGRES_DB,
#                         ) )

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    POSTGRES_SERVER:   str
    POSTGRES_PORT:     int = 5432
    POSTGRES_USER:     str
    POSTGRES_PASSWORD: str
    POSTGRES_DB:       str = ""

    @computed_field
    @property
    def SQLMODEL_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme   = "postgresql+psycopg",
            username = self.POSTGRES_USER,
            password = self.POSTGRES_PASSWORD,
            host     = self.POSTGRES_SERVER,
            port     = self.POSTGRES_PORT,
            path     = self.POSTGRES_DB,
        )
    MAILCHIMP_AUDIENCE_ID:   str
    MAILCHIMP_API_KEY:       str
    MAILCHIMP_SERVER_PREFIX: str


settings = Settings()