from fastapi import HTTPException, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

class User(SQLModel, table=True):
    id:    int | None = Field(default=None, primary_key=True)
    name:  str        = Field(index=True)
    email: str | None = Field(index=True)
    phone: str | None = Field(index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def raise_user_404():
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users/", response_model=list[User])
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise_user_404()
        return user

@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise_user_404()
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise_user_404()
        session.delete(user)
        session.commit()
        return {"ok": True}