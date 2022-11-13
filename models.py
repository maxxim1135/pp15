from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from sqlalchemy import and_

engine = create_engine('mysql://root:123456@localhost:3306/ppdb')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class Demand(Base):
    __tablename__ = "demand"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    medicine_id = Column(ForeignKey("medicines.id"), primary_key=True)
    quantity = Column(Integer)

    child = relationship("Medicine")


# class MedOrd(Base):
#     __tablename__ = "med_ord"
#
#     order_id = Column(ForeignKey("order.id"), primary_key=True)
#     medicine_id = Column(ForeignKey("medicines.id"), primary_key=True)
#     quantity = Column(Integer)
#
#     child = relationship("Medicine")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(45), nullable=False)
    price = Column('price', DECIMAL(10, 2), nullable=False)
    description = Column('description', String(45), nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
    availability = Column('availability', Boolean, nullable=False)


class User(Base):
    __tablename__ = "user"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(45), nullable=False)
    firstName = Column('firstName', String(45), nullable=False)
    lastName = Column('lastName', String(45), nullable=False)
    phone = Column('phone', Integer, nullable=False)
    userStatus = Column('userStatus', Integer, nullable=False)
    email = Column('email', String(45), nullable=False)
    password = Column('password', String(400), nullable=False)

    children = relationship("Demand")


class MedOrder(Base):
    __tablename__ = "medorder"

    id = Column('id', Integer, primary_key=True)
    price = Column('price', DECIMAL(10, 2), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey("user.id"))
    medicine_id = Column('medicine_id', Integer, ForeignKey("medicines.id"))
    quantity = Column(Integer)

    children = relationship("Medicine")

