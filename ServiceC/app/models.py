from sqlalchemy import Column, Integer, Unicode, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    birthdate = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.id"))

    def __init__(self, name, department_id):
        self.name = name
        self.department_id = department_id
