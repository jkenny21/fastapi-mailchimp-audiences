from fastapi import HTTPException, FastAPI
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from app.models import User
from app.db import engine, create_tables
from app.mailchimp import create_audience, create_contact
from app.config import settings

def raise_user_404():
    raise HTTPException(status_code=404, detail="User not found")

def create_mailchimp_contact(user: User):
    member_info = {
        "email_address": user.email,
        "status":        "pending",
        "merge_fields":  {
            "FNAME": user.f_name,
            "LNAME": user.l_name
        }
    }
    create_contact(settings.MAILCHIMP_AUDIENCE_ID, member_info)



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/mailchimp-audiences/")
def create_audience():
    body = {
    "permission_reminder": "You signed up for updates on our website",
    "email_type_option":   False,
    "campaign_defaults":   {
        "from_name":  "Jalen",
        "from_email": "jtkenny21@gmail.com",
        "subject":    "Mailchimp Audience Test",
        "language":   "EN_US"
    },
    "name":    "Mailchimp Audience Test",
    "contact": {
        "company":  "Jalen",
        "address1": "1234 West 1st Ave",
        "city":     "Vancouver",
        "state":    "BC",
        "zip":      "V7J5D5",
        "country":  "CA"
    }
    }
    create_audience(body)

@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        if user.add_to_mailchimp:
            try:
                create_mailchimp_contact(user)
            except:
                raise Exception("Error adding contact to Mailchimp")
            user.add_to_mailchimp = False
            update_user(user.id, user)

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