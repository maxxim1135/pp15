from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from models import *

engine = create_engine('mysql://root:ab?sad132FF..@localhost/mydb')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


users = [
    User(username="BrianMay123", firstName="Brian", lastName="May", phone=1231231231, userStatus=1, email="brianmay@gmail.com", password="oaoa13o132"),
    User(username="JimPage", firstName="Jimmy", lastName="Page", phone=151141241, userStatus=2, email="jimmypage@gmail.com", password="straesthedan")
]

medicines = [
    Medicine(name="Analgin", price=11.5, description="For headache", quantity=100, availability=True),
    Medicine(name="Lizak", price=50, description="For throat ache", quantity=0, availability=False)
]

orders = [
    Order(price=11.5, user_id=1)
]


med_ord = [
    MedOrd(order_id=1, medicine_id=1, quantity=1)
]


demand = [
    Demand(user_id=2, medicine_id=2, quantity=2)
]


def create_users():
    for user in users:
        Session.add(user)
    Session.commit()


def create_med():
    for med in medicines:
        Session.add(med)
    Session.commit()


def create_ord():
    for o in orders:
        Session.add(o)
    Session.commit()


def create_demand():
    for d in demand:
        Session.add(d)
    Session.commit()


def create_medord():
    for m in med_ord:
        Session.add(m)
    Session.commit()


create_users()
create_med()
create_ord()
create_demand()
create_medord()