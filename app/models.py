from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id:               int | None = Field(default=None, primary_key=True)
    name:             str        = Field(index=True)
    email:            str | None = Field(index=True)
    phone:            str | None = Field(index=True)
    marketing_status: str