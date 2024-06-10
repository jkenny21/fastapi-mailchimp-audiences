import os
from dotenv import load_dotenv

from contextlib import asynccontextmanager

from fastapi import HTTPException, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

load_dotenv()



class User(SQLModel, table=True):
    id:               int | None = Field(default=None, primary_key=True)
    name:             str        = Field(index=True)
    email:            str | None = Field(index=True)
    phone:            str | None = Field(index=True)
    marketing_status: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def raise_user_404():
    raise HTTPException(status_code=404, detail="User not found")

async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/mailchimp-audiences/")
def create_audience():
    mailchimp = MailchimpMarketing.Client()
    mailchimp.set_config({
    "api_key": os.environ.get("MAILCHIMP_API_KEY"),
    "server":  os.environ.get("MAILCHIMP_SERVER_PREFIX")
    })

    body = {
    "permission_reminder": "You signed up for updates on our website",
    "email_type_option": False,
    "campaign_defaults": {
        "from_name": "Jalen",
        "from_email": "jtkenny21@gmail.com",
        "subject": "Mailchimp Audience Test",
        "language": "EN_US"
    },
    "name": "Mailchimp Audience Test",
    "contact": {
        "company": "Jalen",
        "address1": "1234 West 1st Ave",
        "city": "Vancouver",
        "state": "BC",
        "zip": "V7J5D5",
        "country": "CA"
    }
    }

    try:
      response = mailchimp.lists.create_list(body)
      print("Response: {}".format(response))
    except ApiClientError as error:
      print("An exception occurred: {}".format(error.text))

@app.post("/mailchimp-contacts")
def create_contact():
    mailchimp = MailchimpMarketing.Client()
    mailchimp.set_config({
    "api_key": os.environ.get("MAILCHIMP_API_KEY"),
    "server":  os.environ.get("MAILCHIMP_SERVER_PREFIX")
    })

    list_id = os.environ.get("MAILCHIMP_AUDIENCE_ID")

    member_info = {
        "email_address": "jtkenny21+testcontact@gmail.com",
        "status": "pending",
        "merge_fields": {
        "FNAME": "Jalen",
        "LNAME": "Kenny"
        }
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


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