from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id:               int | None = Field(default=None, primary_key=True)
    f_name:           str        = Field(index=True)
    l_name:           str        = Field(index=True)
    email:            str | None = Field(index=True)
    add_to_mailchimp: bool       = Field