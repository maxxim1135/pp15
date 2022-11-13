from flask_bcrypt import generate_password_hash
from marshmallow import validate, Schema, fields, ValidationError

from models import *


def validate_id_user(id_user):
    if Session.query(User).filter_by(user_id=id_user).count() == 0:
        return False
    return True


def validate_email(email):
    if not (Session.query(User).filter(User.email == email).count() == 0):
        raise ValidationError("Email exists")


class UserToDo(Schema):
    username = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    phone = fields.Integer()
    userStatus = fields.Integer()
    email = fields.Email(validate=validate_email)
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )


class UserData(Schema):
    id = fields.Integer()
    username = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    phone = fields.Integer()
    userStatus = fields.Integer()


class UserToUpdate(Schema):
    username = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )


class MedicineToDo(Schema):
    name = fields.String()
    price = fields.Integer()
    description = fields.String()
    quantity = fields.Integer()
    availability = fields.Integer()


class MedicineData(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Integer()
    description = fields.String()
    quantity = fields.Integer()
    availability = fields.Integer()


class MedicineToUpdate(Schema):
    name = fields.String()
    price = fields.Integer()
    description = fields.String()
    quantity = fields.Integer()
    availability = fields.Integer()


class MedOrderToDo(Schema):
    medicine_id = fields.Integer()
    user_id = fields.Integer()
    quantity = fields.Integer()
    price = fields.Integer()


class MedOrderData(Schema):
    id = fields.Integer()
    medicine_id = fields.Integer()
    user_id = fields.Integer()
    quantity = fields.Integer()
    price = fields.Integer()


class DemandToDo(Schema):
    user_id = fields.Integer()
    medicine_id = fields.Integer()
    quantity = fields.Integer()


class DemandData(Schema):
    user_id = fields.Integer()
    medicine_id = fields.Integer()
    quantity = fields.Integer()
