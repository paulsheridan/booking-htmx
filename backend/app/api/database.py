from typing import Any

from app.core.security import get_password_hash

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.models import User
from app.api.schemas import UserCreate, UserUpdate
from app.core.security import verify_password


async def create_user(*, session: Session, user_create: UserCreate) -> User:
    print(user_create)
    db_obj = User(
        **user_create.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.execute(statement).first()
    return session_user


def list_users(*, session: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve users.
    """
    count = session.query(User.id).count()
    users = session.query(User).offset(skip).limit(limit).all()

    return (count, users)  # type: ignore # types: ignore


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# def get_user(user_id: str) -> User:
#     table = get_dynamodb_table()

#     user_id_key: str = f"USER#{user_id}"
#     response: dict = table.query(
#         KeyConditionExpression=Key("PK").eq(user_id_key) & Key("SK").eq(user_id_key)
#     )
#     return User(**response["Items"][0])


# def create_or_update_user(user: User) -> User:
#     table = get_dynamodb_table()

#     table.put_item(Item=user.to_item())
#     return user


# def create_or_update_appointment(appointment: Appointment) -> Appointment:
#     table = get_dynamodb_table()
#     # TODO: Make sure there's a legit user attached. I created an appointment with a deleted user
#     table.put_item(Item=appointment.to_item())
#     return appointment


# def get_appointment(user_id: str, start: str) -> Appointment:
#     table = get_dynamodb_table()
#     response = table.query(
#         KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
#         & Key("SK").eq(f"APPT#{start}")
#     )
#     return Appointment(**response["Items"][0])


# def list_appointments(user_id: str, start: str, end: str) -> list[Appointment]:
#     table = get_dynamodb_table()
#     response = table.query(
#         KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
#         & Key("SK").between(f"APPT#{start}", f"APPT#{end}")
#     )
#     return [Appointment(**item) for item in response["Items"]]


# def patch_appointment_status(
#     user_id: str, start: str, confirmed: bool, canceled: bool
# ) -> dict:
#     table = get_dynamodb_table()
#     response = table.update_item(
#         Key={"PK": f"USER#{user_id}", "SK": f"APPT#{start}"},
#         UpdateExpression="SET confirmed=:confirmed, canceled=:canceled",
#         ExpressionAttributeValues={":confirmed": confirmed, ":canceled": canceled},
#         ReturnValues="UPDATED_NEW",
#     )
#     return response


# def create_or_update_client(client: Client) -> Client:
#     table = get_dynamodb_table()

#     table.put_item(Item=client.to_item())
#     return client


# def get_client(user_id: str, email: str) -> Client:
#     table = get_dynamodb_table()

#     response = table.query(
#         KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
#         & Key("SK").eq(f"CLIENT#{email}")
#     )
#     return Client(**response["Items"][0])


# def list_clients(user_id: str) -> list[Client]:
#     table = get_dynamodb_table()

#     response = table.query(
#         KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
#         & Key("SK").begins_with("CLIENT#"),
#     )
#     return [Client(**item) for item in response["Items"]]


# def create_service(service: Service) -> Service:
#     table = get_dynamodb_table()
#     # TODO: validate that dates are in the future, since Service won't anymore.
#     table.put_item(Item=service.to_item())
#     return service


# def get_service(user_id: str, service_id: str) -> Service:
#     table = get_dynamodb_table()

#     response = table.query(
#         KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
#         & Key("SK").eq(f"SRVC#{service_id}")
#     )
#     return Service(**response["Items"][0])